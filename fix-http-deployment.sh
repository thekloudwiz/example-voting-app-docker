#!/bin/bash

# Fix HTTP Deployment Issues Script
# This script fixes CORS, Socket.IO, and security header issues for HTTP deployment

echo "🔧 Fixing HTTP deployment issues..."

# Stop current services
echo "📦 Stopping current services..."
docker-compose down 2>/dev/null || true

# Remove any problematic networks
echo "🌐 Cleaning up networks..."
docker network prune -f

# Rebuild services with fixes
echo "🏗️  Rebuilding services with HTTP fixes..."
docker-compose build --no-cache result

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check service health
echo "🏥 Checking service health..."
echo "Vote service: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health || echo "Not responding")"
echo "Results service: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/health || echo "Not responding")"

# Show service status
echo "📊 Service status:"
docker-compose ps

echo "✅ HTTP deployment fixes applied!"
echo ""
echo "🌐 Your application should now be accessible at:"
echo "   Vote: http://$(curl -s ifconfig.me):5000"
echo "   Results: http://$(curl -s ifconfig.me):5001"
echo ""
echo "🔍 If you still see issues, check the logs with:"
echo "   docker-compose logs result"
echo "   docker-compose logs vote"
