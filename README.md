# Modern Voting App

A completely modernized voting application with contemporary UI/UX, real-time analytics, and production-ready features. Built with modern web technologies and best practices.

## 🚀 Features

### Modern Design & User Experience
- **Contemporary UI**: Glassmorphism design with smooth animations
- **Dark/Light Mode**: System preference detection with manual toggle
- **Fully Responsive**: Mobile-first design that works on all devices
- **Accessibility**: WCAG AA compliant with screen reader support
- **Progressive Web App**: Offline support and installable

### Real-time Analytics
- **Live Updates**: WebSocket connections for instant results
- **Data Visualization**: Interactive charts with Chart.js
- **Enhanced Metrics**: Vote trends, percentages, and analytics
- **Performance Monitoring**: Health checks and system metrics

### Production Ready
- **Security**: Rate limiting, CORS, security headers
- **Performance**: Compression, caching, optimized assets
- **Monitoring**: Redis Insight, pgAdmin, comprehensive logging
- **Testing**: Automated test suite with 11 test categories
- **Deployment**: One-command deployment with Docker Compose

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker and Docker Compose
- 4GB RAM minimum
- Modern web browser

### Start the Application

```bash
# Start the voting app
./deploy.sh

# Or manually with Docker Compose
docker-compose up -d
```

### Access the Applications

| Service | URL | Description |
|---------|-----|-------------|
| **Voting Interface** | http://localhost:5000 | Modern voting UI |
| **Results Dashboard** | http://localhost:5001 | Real-time results with charts |
| **Redis Insight** | http://localhost:8001 | Redis monitoring (with --monitoring) |
| **pgAdmin** | http://localhost:8080 | PostgreSQL admin (with --monitoring) |

## 🧪 Testing

```bash
# Run comprehensive tests
./deploy.sh test

# Or run manually
python3 test-modern-app.py
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Vote App      │    │  Results App    │
│   (Flask)       │    │  (Node.js)      │
│   Port: 5000    │    │   Port: 5001    │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│      Redis      │    │   PostgreSQL    │
│   (Cache/Queue) │    │   (Database)    │
│   Port: 6379    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘
          ▲                      ▲
          │                      │
          └──────────┬───────────┘
                     │
           ┌─────────▼───────┐
           │     Worker      │
           │   (Vote Proc.)  │
           └─────────────────┘
```

**Components:**
- **Vote App**: Modern Python Flask application with enhanced UI
- **Results App**: Node.js application with real-time WebSocket updates
- **Redis**: Caches votes and handles real-time messaging
- **PostgreSQL**: Stores processed votes with connection pooling
- **Worker**: Processes votes from Redis queue to database

## 🎨 Design System

### Color Palette
- **Primary**: Blue gradient (#3b82f6 to #2563eb)
- **Secondary**: Teal gradient (#14b8a6 to #0d9488)
- **Neutral**: Comprehensive gray scale
- **Semantic**: Success, warning, error colors

### Typography
- **Primary Font**: Inter (Google Fonts)
- **Monospace**: JetBrains Mono
- **Scale**: 12 sizes from xs to 6xl

### Components
- **Glassmorphism Cards**: Backdrop blur with subtle borders
- **Interactive Buttons**: Hover states and ripple effects
- **Animated Charts**: Real-time data visualization
- **Progress Indicators**: Loading states and feedback

## 🔧 Configuration

### Environment Variables

```bash
# Vote App
OPTION_A=Cats                    # First voting option
OPTION_B=Dogs                    # Second voting option
REDIS_HOST=redis                 # Redis hostname
SECRET_KEY=your-secret-key       # Flask secret key

# Results App
POSTGRES_HOST=db                 # PostgreSQL hostname
POSTGRES_DB=postgres             # Database name
POSTGRES_USER=postgres           # Database user
POSTGRES_PASSWORD=postgres       # Database password
NODE_ENV=production              # Node environment
```

### Docker Compose Profiles

```bash
# Default services
docker-compose up -d

# Include monitoring services
docker-compose --profile monitoring up -d

# Include nginx load balancer
docker-compose --profile with-nginx up -d
```

## 🛠️ Development

### Local Development

```bash
# Start development environment
./deploy.sh start --monitoring

# View logs
./deploy.sh logs

# Restart services
./deploy.sh restart
```

### File Structure

```
├── vote/                          # Voting application
│   ├── templates/
│   │   └── index.html             # Modern voting UI
│   ├── static/
│   │   ├── stylesheets/
│   │   │   ├── modern-style.css   # Design system
│   │   │   └── voting-interface.css # Voting styles
│   │   └── sw.js                  # Service worker
│   ├── app.py                     # Flask application
│   ├── Dockerfile                 # Container definition
│   └── requirements.txt           # Python dependencies
├── result/                        # Results application
│   ├── views/
│   │   └── index.html             # Results UI with charts
│   ├── server.js                  # Node.js server
│   ├── Dockerfile                 # Container definition
│   └── package.json               # Node.js dependencies
├── worker/                        # Vote processing worker
├── docker-compose.yml             # Service orchestration
├── deploy.sh                      # Deployment script
└── test-modern-app.py             # Test suite
```

## 📊 Monitoring & Health Checks

### Health Endpoints
- **Vote App**: http://localhost:5000/api/health
- **Results App**: http://localhost:5001/api/health

### API Endpoints
- **Vote Stats**: http://localhost:5000/api/stats
- **Results Data**: http://localhost:5001/api/votes

### Monitoring Tools
```bash
# Start with monitoring
./deploy.sh start --monitoring

# Access monitoring tools
# Redis Insight: http://localhost:8001
# pgAdmin: http://localhost:8080 (admin@voting.local / admin)
```

## 🔒 Security Features

- **Helmet.js**: Security headers for Node.js
- **Rate Limiting**: API endpoint protection
- **Input Validation**: Form data sanitization
- **CORS Configuration**: Proper cross-origin settings
- **Container Security**: Non-root users, minimal images

## 🚀 Performance Optimizations

- **Compression**: Gzip compression for responses
- **Caching**: Redis for votes, browser caching for assets
- **Connection Pooling**: PostgreSQL connection management
- **Asset Optimization**: Minified CSS/JS, CDN integration
- **Service Worker**: Offline support and caching

## 🌍 Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+
- **Features**: CSS Grid, Flexbox, Custom Properties, ES6+

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :5000
   
   # Stop conflicting services
   ./deploy.sh stop
   ```

2. **Database connection errors**:
   ```bash
   # Check PostgreSQL logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

3. **Redis connection errors**:
   ```bash
   # Test Redis connection
   docker exec -it voting-redis redis-cli ping
   ```

### Performance Issues

- **Monitor resources**: `docker stats`
- **Check logs**: `./deploy.sh logs`
- **Restart services**: `./deploy.sh restart`

## 📈 Deployment Commands

```bash
# Basic deployment
./deploy.sh

# With monitoring services
./deploy.sh start --monitoring

# Clean deployment (removes old images)
./deploy.sh start --clean-images

# Run tests only
./deploy.sh test

# View service status
./deploy.sh status

# Stop all services
./deploy.sh stop

# View help
./deploy.sh help
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `./deploy.sh test`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Original voting app by Docker team
- Modern UI inspired by contemporary design systems
- Chart.js for data visualization
- Inter font family by Rasmus Andersson
- Font Awesome for icons

---

**Built with ❤️ for modern web development**

