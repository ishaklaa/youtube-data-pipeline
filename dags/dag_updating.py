

from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.data_transform import transform_staging
from scripts.core_updating import updating

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
    transforming_task = PythonOperator(
            task_id='transforming',
            python_callable=transform_staging,
        )
    updating_task = PythonOperator(
                task_id='updating',
                python_callable=updating,
            )
    
staging_task >> transforming_task
transforming_task >> updating_task