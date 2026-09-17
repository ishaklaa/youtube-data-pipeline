
from scripts.channel import build_youtube_client


def get_videos_details(**kwargs):
    youtube = build_youtube_client()
    video_ids = kwargs['ti'].xcom_pull(task_ids='get_videos_data', key='video_ids')

    all_video_data = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        response = youtube.videos().list(
            id=','.join(batch),
            part='snippet,contentDetails,statistics'
        ).execute()

        for item in response['items']:
            all_video_data.append({
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'duration': item['contentDetails']['duration'],
                'view_count': item['statistics'].get('viewCount', 0),
                'like_count': item['statistics'].get('likeCount', 0),
                'comment_count': item['statistics'].get('commentCount', 0),
            })

    kwargs['ti'].xcom_push(key='video_details', value=all_video_data)