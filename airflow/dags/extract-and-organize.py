import os
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

# Criar DAG
with DAG(
    'extract_and_organize',
    default_args=default_args,
    description='Extract and organize',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    execute_meltano_command_csv = DockerOperator(
        task_id='execute_meltano_command_csv',
        image='meltano/meltano:v3.5.4-python3.10',
        command='run extract-and-organize-singer-jsonl-csv',
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
        },
        mount_tmp_dir=False,
        auto_remove='success',
        tty=True,
        retrieve_output=True,
        retrieve_output_path='/data/output/result.json',
    )

    execute_meltano_command_postgres = DockerOperator(
        task_id='execute_meltano_command_postgres',
        image='meltano/meltano:v3.5.4-python3.10',
        command='run extract-and-organize-singer-jsonl-postgres',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mounts=[
            Mount(source='/home/thais/WorkSpaces/Indicium/Entry1/code-challenge/meltano', target='/project',
                  type='bind'),
            Mount(source='/home/thais/WorkSpaces/Indicium/Entry1/code-challenge/data', target='/data', type='bind'),
        ],
        working_dir='/project',
        environment={
            'MELTANO_ENV': 'dev',
        },
        mount_tmp_dir=False,
        auto_remove='success',
        tty=True,
        retrieve_output=True,
        retrieve_output_path='/data/output/result.json',
    )

