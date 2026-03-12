#!/bin/bash

set -e

NETWORK_NAME=reco-network

docker network create ${NETWORK_NAME} 2>/dev/null || true

COMPOSE_FILE="kafka/docker-compose.yml"

# Stop and remove existing Kafka/Zookeeper containers (if any)
docker-compose -f "$COMPOSE_FILE" down -v

# Start Kafka + Zookeeper

echo "Starting Kafka + Zookeeper containers..."
docker-compose -f "$COMPOSE_FILE" up -d

echo "Kafka is available on localhost:9092"
echo "Zookeeper is available on localhost:2181"
