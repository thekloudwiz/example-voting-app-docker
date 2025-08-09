const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { Pool } = require('pg');
const path = require('path');
const compression = require('compression');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// Environment configuration
const PORT = process.env.PORT || 80;
const POSTGRES_HOST = process.env.POSTGRES_HOST || 'db';
const POSTGRES_DB = process.env.POSTGRES_DB || 'postgres';
const POSTGRES_USER = process.env.POSTGRES_USER || 'postgres';
const POSTGRES_PASSWORD = process.env.POSTGRES_PASSWORD || 'postgres';

// Initialize Express app
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://ajax.googleapis.com", "https://cdn.socket.io"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:"]
    }
  }
}));

// Performance middleware
app.use(compression());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // limit each IP to 1000 requests per windowMs (increased for testing)
  message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use(express.static(path.join(__dirname, 'views')));

// PostgreSQL connection pool
const pool = new Pool({
  host: POSTGRES_HOST,
  database: POSTGRES_DB,
  user: POSTGRES_USER,
  password: POSTGRES_PASSWORD,
  port: 5432,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Database connection test
pool.on('connect', () => {
  console.log('Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('PostgreSQL connection error:', err);
});

// Initialize database
async function initializeDatabase() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        vote VARCHAR(1) NOT NULL CHECK (vote IN ('a', 'b')),
        voter_id VARCHAR(255) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // Add unique constraint if it doesn't exist
    await pool.query(`
      DO $$ 
      BEGIN
        IF NOT EXISTS (
          SELECT 1 FROM pg_constraint 
          WHERE conname = 'votes_voter_id_unique'
        ) THEN
          ALTER TABLE votes ADD CONSTRAINT votes_voter_id_unique UNIQUE (voter_id);
        END IF;
      END $$;
    `);
    
    // Create indexes for better performance
    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_votes_timestamp ON votes(timestamp);
    `);
    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_votes_vote ON votes(vote);
    `);
    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_votes_voter_id ON votes(voter_id);
    `);
    
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Database initialization error:', error);
  }
}

// Get vote counts from database
async function getVotes() {
  try {
    const result = await pool.query(`
      SELECT vote, COUNT(*) as count 
      FROM votes 
      GROUP BY vote
    `);
    
    const votes = { a: 0, b: 0 };
    result.rows.forEach(row => {
      if (row.vote === 'a' || row.vote === 'b') {
        votes[row.vote] = parseInt(row.count);
      }
    });
    
    return votes;
  } catch (error) {
    console.error('Error getting votes:', error);
    return { a: 0, b: 0 };
  }
}

// Get vote statistics with additional metrics
async function getVoteStats() {
  try {
    const [voteCounts, totalVotes, recentVotes] = await Promise.all([
      getVotes(),
      pool.query('SELECT COUNT(*) as total FROM votes'),
      pool.query(`
        SELECT vote, COUNT(*) as count 
        FROM votes 
        WHERE timestamp > NOW() - INTERVAL '1 hour'
        GROUP BY vote
      `)
    ]);
    
    const recent = { a: 0, b: 0 };
    recentVotes.rows.forEach(row => {
      if (row.vote === 'a' || row.vote === 'b') {
        recent[row.vote] = parseInt(row.count);
      }
    });
    
    return {
      current: voteCounts,
      total: parseInt(totalVotes.rows[0].total),
      recent: recent,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('Error getting vote stats:', error);
    return {
      current: { a: 0, b: 0 },
      total: 0,
      recent: { a: 0, b: 0 },
      timestamp: new Date().toISOString()
    };
  }
}

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.get('/classic', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.get('/api/votes', async (req, res) => {
  try {
    const stats = await getVoteStats();
    res.json(stats);
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({
      status: 'healthy',
      database: 'connected',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      database: 'disconnected',
      timestamp: new Date().toISOString()
    });
  }
});

// Socket.io connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  // Send initial vote data
  getVotes().then(votes => {
    socket.emit('scores', JSON.stringify(votes));
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Polling function to check for vote updates
let lastVoteCount = 0;

async function pollForUpdates() {
  try {
    const stats = await getVoteStats();
    const currentTotal = stats.total;
    
    if (currentTotal !== lastVoteCount) {
      console.log(`Vote update detected: ${lastVoteCount} -> ${currentTotal}`);
      lastVoteCount = currentTotal;
      
      // Broadcast to all connected clients
      io.emit('scores', JSON.stringify(stats.current));
      
      // Broadcast additional stats for enhanced clients
      io.emit('stats', JSON.stringify(stats));
    }
  } catch (error) {
    console.error('Polling error:', error);
  }
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
    timestamp: new Date().toISOString()
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('HTTP server closed');
    pool.end(() => {
      console.log('Database pool closed');
      process.exit(0);
    });
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  server.close(() => {
    console.log('HTTP server closed');
    pool.end(() => {
      console.log('Database pool closed');
      process.exit(0);
    });
  });
});

// Start server
async function startServer() {
  try {
    await initializeDatabase();
    
    server.listen(PORT, () => {
      console.log(`Modern results server listening on port ${PORT}`);
      console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
      
      // Start polling for updates every 1 second
      setInterval(pollForUpdates, 1000);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
