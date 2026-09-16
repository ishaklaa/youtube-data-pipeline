import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host='localhost',  
    port=os.getenv('POSTGRES_CONN_PORT'),
    dbname=os.getenv('ELT_DATABASE_NAME'),
    user=os.getenv('ELT_DATABASE_USERNAME'),
    password=os.getenv('ELT_DATABASE_PASSWORD')
)
cur = conn.cursor()

cur.execute("""
   

    CREATE TABLE IF NOT EXISTS staging (
        video_id TEXT,
        title TEXT,
        published_at TEXT,
        duration TEXT,
        view_count TEXT,
        like_count TEXT,
        comment_count TEXT,
        loaded_at TIMESTAMP DEFAULT NOW()
    );
""")

conn.commit()
cur.close()
conn.close()

print("Table staging créée avec succès")