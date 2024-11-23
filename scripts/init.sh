#!/bin/bash

# Function to display usage information
usage() {
  echo "Usage: $0 --meltano-path <path> --data-path <path>"
  exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --meltano-path) MELTANO_PATH="$2"; shift ;;
    --data-path) DATA_PATH="$2"; shift ;;
    *) usage ;;
  esac
  shift
done

# Validate arguments
if [[ -z "$MELTANO_PATH" || -z "$DATA_PATH" ]]; then
  usage
fi

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

