from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from scripts.channel import get_channel
from scripts.videos import get_videos
from scripts.videos_details import get_videos_details
from scripts.json_creation import create_json_file


default_args = {
    'owner': 'airflow',
    'retries': 1,
}


with DAG(
    dag_id='youtube_extraction',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 9, 1),
    catchup=False,
    tags=['youtube', 'extraction'],
) as dag:

    get_channel_task = PythonOperator(
        task_id='get_channel',
        python_callable=get_channel,
    )

    get_videos_task = PythonOperator(
        task_id='get_videos_data',
        python_callable=get_videos,
    )

    get_videos_details_task = PythonOperator(
        task_id='get_videos_details',
        python_callable=get_videos_details,
    )

    create_json_file_task = PythonOperator(
        task_id='create_json_file',
        python_callable=create_json_file,
    )

    trigger_staging = TriggerDagRunOperator(
        task_id='trigger_youtube_updating',
        trigger_dag_id='youtube_data_updating',
        wait_for_completion=False,
    )

    
    get_channel_task >> get_videos_task >> get_videos_details_task >> create_json_file_task >> trigger_staging