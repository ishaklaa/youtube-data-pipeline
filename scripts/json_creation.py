# scripts/json_creation.py
from datetime import datetime
import os
import json


def create_json_file(**kwargs):
    all_video_data = kwargs['ti'].xcom_pull(task_ids='get_videos_details', key='video_details')

    os.makedirs('/opt/airflow/data', exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M')
    output_path = f'/opt/airflow/data/YTdata{date_str}.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_video_data, f, indent=2, ensure_ascii=False)

    kwargs['ti'].xcom_push(key='json_path', value=output_path)