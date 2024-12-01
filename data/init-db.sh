#!/bin/bash
set -e

# Create databases
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE northwind;
    CREATE DATABASE northwind_target;
EOSQL

# Create users and grant permissions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="northwind" <<-EOSQL
    CREATE USER northwind_user WITH PASSWORD 'thewindisblowing';
    GRANT ALL PRIVILEGES ON DATABASE northwind TO northwind_user;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="northwind_target" <<-EOSQL
    CREATE USER northwind_target_user WITH PASSWORD 'thewindisblowing';
    GRANT ALL PRIVILEGES ON DATABASE northwind_target TO northwind_target_user;
EOSQL

# Restore northwind.sql into the northwind database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="northwind" < /docker-entrypoint-initdb.d/northwind.sql

# Grant permissions on all tables to northwind_user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="northwind" <<-EOSQL
    GRANT USAGE ON SCHEMA public TO northwind_user;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO northwind_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO northwind_user;
EOSQL
