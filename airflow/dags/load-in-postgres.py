import os
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount


# Configurações padrão
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Obter a data atual no formato desejado (YYYY-MM-DD)
current_date = datetime.now().strftime('%Y-%m-%d')

# Criar DAG
with DAG(
    'load_in_postgres',
    default_args=default_args,
    description='Extract and organize',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    execute_meltano_command = DockerOperator(
        task_id='execute_meltano_command',
        image='meltano/meltano:v3.5.4-python3.10',
        command=f'run load-in-postgres',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mounts=[
            Mount(source='/home/thais/WorkSpaces/Indicium/Entry1/code-challenge/meltano', target='/project', type='bind'),
            Mount(source='/home/thais/WorkSpaces/Indicium/Entry1/code-challenge/data', target='/data', type='bind'),
        ],
        working_dir='/project',
        environment={
            'MELTANO_ENV': 'dev',
            'RUN_DATE': current_date,
            'DATABASE_URL': 'postgresql://u29ab7pcgqhpbv:pdd8a4078df84ad3d403aee1aacdc24e45075213d63f0c4d20d6164eaa260cade@cc0gj7hsrh0ht8.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6fdgb0dvupqmd'

        },
        mount_tmp_dir=False,
        auto_remove='success',
        tty=True,
        retrieve_output=True,
        retrieve_output_path='/data/output/result.json',
    )