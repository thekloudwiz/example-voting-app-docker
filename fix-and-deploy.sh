#!/bin/bash

# Single script to fix all issues and deploy
# Fixes: 1) Pre-selected vote 2) Sound length 3) Results showing zero

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

echo "✅ Deployment complete!"
echo "🌐 Vote: http://localhost:5000 (or your EC2 IP:5000)"
echo "📊 Results: http://localhost:5001 (or your EC2 IP:5001)"
