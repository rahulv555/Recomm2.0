#!/bin/bash

NETWORK_NAME=reco-network

docker network create ${NETWORK_NAME} 2>/dev/null || true
# Stop and remove existing containers and networks
docker-compose down

# Build (if needed) and start Redis + ml-service in detached mode
echo "Starting ml-service + Redis containers..."
docker-compose up -d --build

echo "Redis is accessible on port 6379"
echo "ml-service is accessible on port 8088 (uvicorn)"
