#!/bin/bash

APP_NAME=apigateway
IMAGE_NAME=prodrecomm-apigatway
CONTAINER_NAME=prodrecomm-apigatway
PORT=4005
NETWORK_NAME=reco-network

# Create a network if it doesn't exist so containers can talk to each other
docker network create ${NETWORK_NAME} 2>/dev/null || true

echo "Building jar..."
./mvnw clean package -DskipTests

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Stopping existing container (if running)..."
docker stop $CONTAINER_NAME || true

echo "Removing old container..."
docker rm $CONTAINER_NAME || true

echo "Starting new container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:4005 \
  --network ${NETWORK_NAME} \
  $IMAGE_NAME

echo "Deployment complete!"