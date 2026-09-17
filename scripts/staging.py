
import glob
import json
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
from airflow.providers.postgres.hooks.postgres import PostgresHook


def staging():
    data_dir = Path('/opt/airflow/data')
    json_files = sorted(data_dir.glob("YTdata*.json"))
    if not json_files:
        raise FileNotFoundError(f"No YTdata*.json file found in {data_dir}")
    latest_file = json_files[-1]

    with open(latest_file, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    print(len(videos))

    hook = PostgresHook(postgres_conn_id='postgres_db_yt_elt')
    hook.insert_rows(
        table='staging',
        rows=[
            (
                video['video_id'],
                video['title'],
                video['published_at'],
                video['duration'],
                str(video['view_count']),
                str(video['like_count']),
                str(video['comment_count'])
            )
            for video in videos
        ],
        target_fields=[
            "video_id", "title", "published_at", "duration",
            "view_count", "like_count", "comment_count"
        ],
        replace=True,
        replace_index='video_id',
    )
