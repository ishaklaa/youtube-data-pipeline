import re
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def parse_duration(duration_str):
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration_str)
    if not match or match.group(0) == '':
        return 0
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds


def get_staging_data():
   
    hook = PostgresHook(postgres_conn_id='postgres_db_yt_elt')
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM staging;")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data = []
    for row in rows:
        video_dict = dict(zip(columns, row))
        data.append(video_dict)

    cursor.close()
    conn.close()

    return data


def transform_staging(**kwargs):
    data = get_staging_data()
    df = pd.DataFrame(data)

    df["published_at"] = pd.to_datetime(df["published_at"], format='mixed')
    df["published_at"] = df["published_at"].dt.strftime('%Y-%m-%dT%H:%M:%S')
    df["loaded_at"] = pd.to_datetime(df["loaded_at"])
    df["loaded_at"] = df["loaded_at"].dt.strftime('%Y-%m-%dT%H:%M:%S')
    df["view_count"] = df["view_count"].astype(int)
    df["like_count"] = df["like_count"].astype(int)
    df["comment_count"] = df["comment_count"].astype(int)
    df["duration"] = df["duration"].apply(parse_duration)
    records = df.to_dict(orient='records')

    kwargs["ti"].xcom_push(key='transformed_data', value=records)
    return records