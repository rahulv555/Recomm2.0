# Setup db
chmod +x ./db/setup_postgres.sh
chmod +x ./apigateway/apigateway/build_image_run_container.sh
./db/setup_postgres.sh

source .venv/Scripts/activate
.venv/Scripts/python datasetup.py


