from googleapiclient.discovery import build
import json
from datetime import datetime


api_key = "AIzaSyCbRCbf6TSQzZWhUXSMtMxjEt_9RwEmRJA"
youtube = build('youtube','v3',developerKey = api_key)

channel_id = 'UC0WP5P-ufpRfjbNrmOWwLBQ'

channel_response = youtube.channels().list(
    id=channel_id,
    part='contentDetails'
).execute()

uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
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
    

all_video_data = []

for i in range(0, len(video_ids), 50):
    batch = video_ids[i:i+50]
    response = youtube.videos().list(
        id=','.join(batch),
        part='snippet,contentDetails,statistics'
    ).execute()

    for item in response['items']:
        video_data = {
            'video_id': item['id'],
            'title': item['snippet']['title'],
            'published_at': item['snippet']['publishedAt'],
            'duration': item['contentDetails']['duration'],
            'view_count': item['statistics'].get('viewCount', 0),
            'like_count': item['statistics'].get('likeCount', 0),
            'comment_count': item['statistics'].get('commentCount', 0),
        }
        all_video_data.append(video_data)


     
date_str = datetime.now().strftime('%Y-%m-%d')
output_path = f'data/YTdata{date_str}.json'

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_video_data, f, indent=2, ensure_ascii=False)

print(f"Données sauvegardées dans {output_path}")