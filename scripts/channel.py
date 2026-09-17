# scripts/channel.py
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


def build_youtube_client():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return build('youtube', 'v3', developerKey=api_key)


def get_channel(**kwargs):
    youtube = build_youtube_client()
    channel_id = 'UC0WP5P-ufpRfjbNrmOWwLBQ'

    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    kwargs['ti'].xcom_push(key='uploads_playlist_id', value=uploads_playlist_id)
