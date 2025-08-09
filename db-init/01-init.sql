-- Initialize the voting database
-- This script creates the necessary tables for the voting application

-- Create the votes table
CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    vote VARCHAR(1) NOT NULL CHECK (vote IN ('a', 'b')),
    voter_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_votes_vote ON votes(vote);
CREATE INDEX IF NOT EXISTS idx_votes_voter_id ON votes(voter_id);
CREATE INDEX IF NOT EXISTS idx_votes_timestamp ON votes(timestamp);

-- Create a unique constraint to prevent duplicate votes from the same voter
-- (Optional: uncomment if you want to prevent multiple votes per voter)
-- CREATE UNIQUE INDEX IF NOT EXISTS idx_votes_unique_voter ON votes(voter_id);

-- Insert some sample data for testing (optional)
-- INSERT INTO votes (vote, voter_id) VALUES 
--     ('a', 'sample-voter-1'),
--     ('b', 'sample-voter-2'),
--     ('a', 'sample-voter-3')
-- ON CONFLICT DO NOTHING;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON TABLE votes TO postgres;
GRANT USAGE, SELECT ON SEQUENCE votes_id_seq TO postgres;

-- Display table structure for verification
\d votes;

-- Display current vote counts
SELECT vote, COUNT(*) as count FROM votes GROUP BY vote;
