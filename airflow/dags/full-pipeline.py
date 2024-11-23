from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Argumentos padrão para o DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Criar a DAG
with DAG(
    'full_pipeline',
    default_args=default_args,
    description='Executa a pipeline completa com dependências entre DAGs.',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Executar a primeira DAG
    trigger_extract_and_organize = TriggerDagRunOperator(
        task_id='trigger_extract_and_organize',
        trigger_dag_id='extract_and_organize',
        wait_for_completion=True,
        poke_interval=30,
        allowed_states=['success'],
        failed_states=['failed'],
    )

    # Executar a segunda DAG apenas após a primeira DAG completar com sucesso
    trigger_load_in_postgres = TriggerDagRunOperator(
        task_id='trigger_load_in_postgres',
        trigger_dag_id='load_in_postgres',
        wait_for_completion=True,
        poke_interval=30,
        allowed_states=['success'],
        failed_states=['failed'],
    )

    # Definir dependências
    trigger_extract_and_organize >> trigger_load_in_postgres
