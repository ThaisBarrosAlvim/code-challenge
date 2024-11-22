#!/bin/bash

# Informações de conexão
DB_NAME="northwind_target"
DB_HOST="dpg-ct0c0q5umphs73f3tcrg-a.oregon-postgres.render.com"
DB_PORT="5432"
DB_USER="northwind_target_user"
DB_PASSWORD="8pod2pzmPmnzSCEU5b1KnC0aKwxh9Tk4"
SCHEMA="public"

# Exporta a senha para evitar prompts
export PGPASSWORD="$DB_PASSWORD"

# Conexão ao banco e exclusão de tabelas
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
DO
\$\$
DECLARE
    tabela RECORD;
BEGIN
    -- Loop por todas as tabelas no schema 'public'
    FOR tabela IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = '$SCHEMA'
    LOOP
        -- Exclui a tabela
        EXECUTE format('DROP TABLE IF EXISTS %I.%I CASCADE;', '$SCHEMA', tabela.tablename);
    END LOOP;
END
\$\$;
EOF

# Limpa a variável de senha
unset PGPASSWORD

echo "Todas as tabelas do schema '$SCHEMA' foram excluídas do banco '$DB_NAME'."
