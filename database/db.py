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
    drop table staging;
    drop table core;
    CREATE TABLE IF NOT EXISTS staging (
        video_id VARCHAR PRIMARY KEY,  
        title TEXT,
        published_at TEXT,
        duration TEXT,
        view_count TEXT,
        like_count TEXT,
        comment_count TEXT,
        loaded_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE TABLE IF NOT EXISTS core (
        video_id VARCHAR PRIMARY KEY,  
        title TEXT,
        published_at TIMESTAMP,
        duration INTEGER,
        view_count BIGINT,
        like_count BIGINT,
        comment_count BIGINT,
        loaded_at TIMESTAMP
    );
""")

conn.commit()
cur.close()
conn.close()

print("Table staging créée avec succès")