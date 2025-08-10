#!/bin/bash

# Complete SSL/HTTP Deployment Fix Script
# Fixes ERR_SSL_PROTOCOL_ERROR and connection issues

echo "🔧 Fixing SSL protocol errors and connection issues..."

# Stop all services
echo "🛑 Stopping all services..."
docker-compose down --remove-orphans

# Remove all containers and networks
echo "🧹 Cleaning up containers and networks..."
docker container prune -f
docker network prune -f

# Remove and rebuild images to ensure fresh deployment
echo "🏗️  Rebuilding all services from scratch..."
docker-compose build --no-cache --pull

# Start services with explicit HTTP configuration
echo "🚀 Starting services with HTTP configuration..."
docker-compose up -d

# Wait for services to initialize
echo "⏳ Waiting for services to initialize..."
sleep 20

# Check if services are responding
echo "🏥 Checking service health..."

# Test vote service
VOTE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health 2>/dev/null || echo "000")
echo "Vote service (port 5000): HTTP $VOTE_STATUS"

# Test result service
RESULT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/health 2>/dev/null || echo "000")
echo "Result service (port 5001): HTTP $RESULT_STATUS"

# Test API endpoint
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/votes 2>/dev/null || echo "000")
echo "API endpoint (/api/votes): HTTP $API_STATUS"

# Show container status
echo ""
echo "📊 Container status:"
docker-compose ps

# Show service logs if there are issues
if [ "$RESULT_STATUS" != "200" ] || [ "$API_STATUS" != "200" ]; then
    echo ""
    echo "⚠️  Issues detected. Showing recent logs:"
    echo "--- Result Service Logs ---"
    docker-compose logs --tail=20 result
fi

# Get public IP for external access
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "YOUR_EC2_IP")

echo ""
echo "✅ HTTP deployment fix completed!"
echo ""
echo "🌐 Access your application at:"
echo "   Vote: http://$PUBLIC_IP:5000"
echo "   Results: http://$PUBLIC_IP:5001"
echo ""
echo "🔍 If issues persist, check browser console and run:"
echo "   docker-compose logs result"
echo "   docker-compose logs vote"
echo ""
echo "💡 Make sure your EC2 security group allows inbound traffic on ports 5000 and 5001"
