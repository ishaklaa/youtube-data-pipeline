import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


with open('data/YTdata2026-09-16.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)


conn = psycopg2.connect(
    host='localhost',  
    port=os.getenv('POSTGRES_CONN_PORT'),
    dbname=os.getenv('ELT_DATABASE_NAME'),
    user=os.getenv('ELT_DATABASE_USERNAME'),
    password=os.getenv('ELT_DATABASE_PASSWORD')
)
cur = conn.cursor()


for video in videos:
    cur.execute("""
        INSERT INTO staging (video_id, title, published_at, duration, view_count, like_count, comment_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        video['video_id'],
        video['title'],
        video['published_at'],
        video['duration'],
        str(video['view_count']),
        str(video['like_count']),
        str(video['comment_count'])
    ))

conn.commit()
cur.close()
conn.close()

print(f"{len(videos)} vidéos chargées dans videos")