#!/usr/bin/env bash
set -e

CONTAINER_NAME=reco-postgres
POSTGRES_USER=reco_user
POSTGRES_PASSWORD=reco_pass
POSTGRES_DB=reco_db
POSTGRES_PORT=5432  
VOLUME='E:\Recomm2.0\dbvolumes'
NETWORK_NAME=reco-network

# Create a network if it doesn't exist so containers can talk to each other
docker network create ${NETWORK_NAME} 2>/dev/null || true


echo "▶ Checking if container exists..."

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "✔ Container exists"

    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo "✔ Container already running"
    else
        echo "▶ Starting existing container..."
        docker start $CONTAINER_NAME
    fi
else
    echo "▶ Creating new PostgreSQL container..."
    docker run -d \
        --name $CONTAINER_NAME \
        -e POSTGRES_USER=$POSTGRES_USER \
        -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
        -e POSTGRES_DB=$POSTGRES_DB \
        -p $POSTGRES_PORT:5432 \
        -v $VOLUME:/var/lib/postgresql/ \
        --network ${NETWORK_NAME} \
        postgres:latest
fi

echo "▶ Waiting for PostgreSQL to be ready..."

until docker exec $CONTAINER_NAME pg_isready -U $POSTGRES_USER > /dev/null 2>&1; do
    sleep 1
done

echo "✔ PostgreSQL is ready"

echo "▶ Creating tables (if not exists)..."

docker exec -i $CONTAINER_NAME psql \
    -U $POSTGRES_USER \
    -d $POSTGRES_DB \
    < db/init_reco.sql

echo "✅ PostgreSQL setup complete"