# Indicium Tech Code Challenge: Building a Robust Data Pipeline

<p align="center">
  <img src="https://raw.githubusercontent.com/ThaisBarrosAlvim/code-challenge/refs/heads/main/docs/diagrama_embulk_meltano.jpg" />
</p>

[![codebeat badge](https://codebeat.co/badges/ca249cd6-ef5a-4933-affe-3be6ded2e737)](https://codebeat.co/projects/github-com-thaisbarrosalvim-code-challenge-main)

* [Video Overview](https://youtu.be/ImPN6BImJOU)

This project implements a robust data pipeline to extract, store, and load data from two sources (a PostgreSQL database and a CSV file) into a PostgreSQL database. The pipeline uses **Airflow** for orchestration, **Meltano** for data handling, and **PostgreSQL** as the storage backend. The focus is on modularity, idempotency, and adaptability, making it suitable for real-world scenarios.



## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup](#setup)
5. [Usage](#usage)
6. [Future Improvements](#future-improvements)

---

## Overview
This pipeline processes data by extracting it from two sources:
- A PostgreSQL database (Northwind schema).
- A CSV file representing the `order_details` table.

The pipeline writes this data to local storage (organized by source, table, and date) and subsequently loads it into a PostgreSQL database. Airflow DAGs orchestrate the workflow, ensuring step dependencies are maintained.

---

## Features
- **Data Extraction**:
  - Supports extracting all tables from the PostgreSQL source database.
  - Extracts `order_details` from the CSV file.
- **Data Storage**:
  - Writes extracted data in **Singer JSONL** format to local storage, organized by source, table, and execution date.
- **Data Loading**:
  - Loads the Singer JSONL files into the target PostgreSQL database.
- **Orchestration**:
  - Airflow DAGs handle step dependencies, ensuring proper execution order.
- **Historical Reprocessing**:
  - Allows reprocessing for specific past dates with a configurable execution date.

---

## Requirements
- **Docker & Docker Compose**
- **Airflow**: For task scheduling and orchestration.
- **Meltano**: For data extraction and loading.
- **PostgreSQL**: As source and target databases.
---

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ThaisBarrosAlvim/code-challenge.git
   cd code-challenge
   ```

2. **Update Airflow Permissions**:
   ```bash
   sudo chmod u=rwx,g=rwx,o=rwx -R airflow/
   sudo chmod 777 /var/run/docker.sock
   ```

3. **Start Services**:
   ```bash
   docker compose up -d
   ```

4. **Configure Meltano**:
   ```bash
   docker compose exec meltano meltano lock --update --all
   docker compose exec meltano meltano install
   ```

5. **Set Airflow ENV Vars (put your full path)**:
    ```bash
    docker compose exec airflow-scheduler airflow variables set HOST_PATH_MELTANO "/home/yourname/folder/code-challenge/meltano"
    docker compose exec airflow-scheduler airflow variables set HOST_PATH_DATA "/home/yourname/folder/code-challenge/data"
    ```

6. **Access the Airflow UI**:
   - **URL**: `http://localhost:8080`
   - **Credentials**: `admin / admin`

---

## Usage

### Running the Pipeline
#### Step 1: Data Extraction
Run the extraction jobs using Meltano:
```bash
docker compose exec meltano meltano run extract-and-organize-singer-jsonl-csv
docker compose exec meltano meltano run extract-and-organize-singer-jsonl-postgres
```

#### Step 2: Data Loading
Load the extracted data into the target PostgreSQL database:
```bash
docker compose exec meltano meltano run load-in-postgres
```

### Orchestrating with Airflow
Trigger the pipeline steps through Airflow DAGs:
- Trigger the extraction DAG:
  ```bash
  docker compose exec airflow-webserver airflow dags trigger extraction_dag
  ```
- Trigger the loading DAG:
  ```bash
  docker compose exec airflow-webserver airflow dags trigger loading_dag
  ```
- Trigger the full pipeline DAG:
  ```bash
  docker compose exec airflow-webserver airflow dags trigger full_pipeline_dag
  ```

### Reprocessing for Past Days
Reprocess data for a specific past date using the `RUN_DATE` environment variable:
```bash
docker compose exec meltano RUN_DATE=2024-11-23 meltano run load-in-postgres
```

---

## Future Improvements
1. **Local Database Integration**:
   - Due to limitations with `psycopg2` in the **target-postgres** and **tap-postgres** plugins when integrating Meltano with Airflow via Docker Operator, we had to use external PostgreSQL databases hosted on [Render](https://render.com/). This issue has been reported in the MeltanoLabs repository ([target-postgres issue #433](https://github.com/MeltanoLabs/target-postgres/issues/433)) and matches a similar problem discussed on [StackOverflow](https://stackoverflow.com/q/71116549).
   - The error prevents successful connections to a local PostgreSQL instance in this setup. Resolving this issue would enable the use of local databases, improving performance, reducing external dependencies, and simplifying the deployment process.

