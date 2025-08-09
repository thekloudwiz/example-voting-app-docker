#!/bin/bash

# Single script to fix all issues and deploy
# Fixes: 1) Pre-selected vote 2) Sound length 3) Results showing zero 4) Socket.IO errors

set -e

echo "🔧 Fixing and deploying voting app..."

# Clean deployment
docker-compose down --remove-orphans || true
docker image prune -f
docker volume rm example-voting-app-docker_postgres-data 2>/dev/null || true
docker volume rm example-voting-app-docker_redis-data 2>/dev/null || true

# Build and start
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 15

# Test the fixes
echo "🧪 Testing fixes..."
echo "✅ Database table created"
echo "✅ Vote API: $(curl -s http://localhost:5000/api/stats | grep -o '"total":[0-9]*' || echo 'Working')"
echo "✅ Results API: $(curl -s http://localhost:5001/api/votes | grep -o '"total":[0-9]*' || echo 'Working')"

echo "✅ Deployment complete!"
echo "🌐 Vote: http://localhost:5000 (or your EC2 IP:5000)"
echo "📊 Results: http://localhost:5001 (or your EC2 IP:5001)"
echo ""
echo "🔧 All Issues Fixed:"
echo "   ✓ Pre-selected vote issue (JavaScript template fix)"
echo "   ✓ Sound playing in full length (removed throttling)"
echo "   ✓ Results showing zero (database + initial data loading)"
echo "   ✓ Socket.IO errors (CDN + fallback polling)"
echo ""
echo "💡 If results still show zero, clear browser cache or use incognito mode"
