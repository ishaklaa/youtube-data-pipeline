from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.staging import staging

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='youtube_data_updating',
    default_args=default_args,
    tags=['youtube', 'staging'],
) as dag:

    staging_task = PythonOperator(
        task_id='load_staging',
        python_callable=staging,
    )