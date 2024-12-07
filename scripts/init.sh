#!/bin/bash

# Get current script directory
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Set paths based on script location
MELTANO_PATH="$SCRIPT_DIR/../meltano"
DATA_PATH="$SCRIPT_DIR/../data"

# Start Docker services
docker compose up -d

# Update Airflow permissions
sudo chmod u=rwx,g=rwx,o=rwx -R airflow/
sudo chmod 777 /var/run/docker.sock

# Restart Docker services to update airflow paths with the permissions
docker compose restart

# Configure Meltano
docker compose exec meltano meltano lock --update --all
docker compose exec meltano meltano install

# Set Airflow environment variables
docker compose exec airflow-scheduler airflow variables set HOST_PATH_MELTANO "$MELTANO_PATH"
docker compose exec airflow-scheduler airflow variables set HOST_PATH_DATA "$DATA_PATH"

# Provide feedback to the user
echo "Setup completed successfully. Access Airflow UI at http://localhost:8080 with credentials: admin / admin."

