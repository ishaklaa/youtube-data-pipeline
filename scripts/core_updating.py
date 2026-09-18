from airflow.providers.postgres.hooks.postgres import PostgresHook


def updating(**kwargs):
    videos = kwargs['ti'].xcom_pull(task_ids='transforming', key='transformed_data')
    
    hook = PostgresHook(postgres_conn_id='postgres_db_yt_elt')
    hook.insert_rows(
        table='core',
        rows=[
            (
                video['video_id'],
                video['title'],
                video['published_at'],
                video['duration'],
                video['view_count'],
                video['like_count'],
                video['comment_count'],
                video['loaded_at'],
            )
            for video in videos
        ],
        target_fields=[
            "video_id", "title", "published_at", "duration",
            "view_count", "like_count", "comment_count", "loaded_at"
        ],
        replace=True,
        replace_index='video_id',
    )