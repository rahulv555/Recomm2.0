#!/bin/bash
## Only run after setting up DB, waiting for it to start, running datasetup.py and then training.ipynb


set -e

echo "=== Starting apigateway ==="
cd apigateway/apigateway
./build_image_run_container.sh
cd -

./setup-kafka.sh


echo "=== Starting ml-service + Redis ==="
cd ml-service
./setup.sh
cd -

echo "=== Starting recommservice ==="
cd recommservice
./setup.sh
cd -

echo "=== Starting restaurantservice ==="
cd restaurantservice
./setup.sh
cd -

echo "=== Starting userservice ==="
cd userservice
./setup.sh
cd -

echo "All services started."
