# scripts/videos.py
from scripts.channel import build_youtube_client


def get_videos(**kwargs):
    youtube = build_youtube_client()
    uploads_playlist_id = kwargs['ti'].xcom_pull(task_ids='get_channel', key='uploads_playlist_id')

    video_ids = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='contentDetails',
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        for item in playlist_response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    kwargs['ti'].xcom_push(key='video_ids', value=video_ids)