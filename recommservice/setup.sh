#!/bin/bash

set -e

SERVICE_NAME=recommservice
IMAGE_NAME=${SERVICE_NAME}:latest
CONTAINER_NAME=recomm-${SERVICE_NAME}
NETWORK_NAME=reco-network

# Create a network if it doesn't exist so containers can talk to each other
docker network create ${NETWORK_NAME} 2>/dev/null || true

echo "Building ${SERVICE_NAME} image..."
docker build -t ${IMAGE_NAME} .

echo "Stopping any existing ${CONTAINER_NAME}..."
docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

echo "Starting ${SERVICE_NAME} container (host port 8087 -> container 8087)..."
docker run -d --name ${CONTAINER_NAME} -p 8087:8087 -e ML_SERVICE_URL=http://ml_service:8088 -e ml.service.url=http://ml_service:8088 -e SPRING_KAFKA_BOOTSTRAP_SERVERS=kafka:29092 -e SPRING_KAFKA_CONSUMER_KEY_DESERIALIZER=org.apache.kafka.common.serialization.StringDeserializer -e SPRING_KAFKA_CONSUMER_VALUE_DESERIALIZER=org.apache.kafka.common.serialization.ByteArrayDeserializer \
    -e SPRING_DATASOURCE_URL=jdbc:postgresql://reco-postgres:5432/reco_db \
  -e SPRING_DATASOURCE_USERNAME=reco_user \
  -e SPRING_DATASOURCE_PASSWORD=reco_pass \
  -e SPRING_JPA_HIBERNATE_DDL_AUTO=update \
  -e SPRING_KAFKA_CONSUMER_GROUP_ID=recomm-service \
  -e SPRING_KAFKA_CONSUMER_AUTO_OFFSET_RESET=earliest \
  --network ${NETWORK_NAME} \
  ${IMAGE_NAME}

echo "${SERVICE_NAME} is running at http://localhost:8087"
