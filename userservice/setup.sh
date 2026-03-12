#!/bin/bash

set -e

SERVICE_NAME=userservice
IMAGE_NAME=${SERVICE_NAME}:latest
CONTAINER_NAME=recomm-${SERVICE_NAME}
NETWORK_NAME=reco-network

docker network create ${NETWORK_NAME} 2>/dev/null || true

echo "Building ${SERVICE_NAME} image..."
docker build -t ${IMAGE_NAME} .

echo "Stopping any existing ${CONTAINER_NAME}..."
docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

echo "Starting ${SERVICE_NAME} container (host port 8085 -> container 8085)..."
docker run -d --name ${CONTAINER_NAME} --network ${NETWORK_NAME} -p 8085:8085 -e SPRING_KAFKA_BOOTSTRAP_SERVERS=kafka:29092 -e SPRING_KAFKA_PRODUCER_KEY_SERIALIZER=org.apache.kafka.common.serialization.StringSerializer -e SPRING_KAFKA_PRODUCER_VALUE_SERIALIZER=org.apache.kafka.common.serialization.ByteArraySerializer \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://reco-postgres:5432/reco_db \
  -e SPRING_DATASOURCE_USERNAME=reco_user \
  -e SPRING_DATASOURCE_PASSWORD=reco_pass \
  -e SPRING_JPA_HIBERNATE_DDL_AUTO=update \
   ${IMAGE_NAME} 

echo "${SERVICE_NAME} is running at http://localhost:8085"
