#!/bin/bash

set -e

SERVICE_NAME=restaurantservice
IMAGE_NAME=${SERVICE_NAME}:latest
CONTAINER_NAME=recomm-${SERVICE_NAME}
NETWORK_NAME=reco-network

# Create a network if it doesn't exist so containers can talk to each other
docker network create ${NETWORK_NAME} 2>/dev/null || true

echo "Building ${SERVICE_NAME} image..."
docker build -t ${IMAGE_NAME} .

echo "Stopping any existing ${CONTAINER_NAME}..."
docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

echo "Starting ${SERVICE_NAME} container (host port 8086 -> container 8086)..."
docker run -d --name ${CONTAINER_NAME} -p 8086:8086 -e SPRING_DATASOURCE_URL=jdbc:postgresql://reco-postgres:5432/reco_db -e SPRING_DATASOURCE_USERNAME=reco_user -e SPRING_DATASOURCE_PASSWORD=reco_pass -e SPRING_JPA_HIBERNATE_DDL_AUTO=update --network ${NETWORK_NAME} ${IMAGE_NAME}

echo "${SERVICE_NAME} is running at http://localhost:8086"
