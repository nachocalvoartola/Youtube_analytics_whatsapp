import os
import googleapiclient.discovery
from twilio_rest import Client
from config import YOUTUBE_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER_TO, PHONE_NUMBER_FROM


 # Get videos in the "most popular" category for the past 24 hours

def get_most_watched_videos(max_results, region):
    youtube = googleapiclient.discovery.build('youtube', 'v3', YOUTUBE_API_KEY)

   
    request = youtube.videos().list(
        part='snippet,statistics',  # Include 'statistics' to get viewCount and likeCount
        chart='mostPopular',
        regionCode=region,
        maxResults=max_results
    )

    response = request.execute()

    # Extract the title, link, viewCount, and likeCount of each video
    videos = []
    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        view_count = item['statistics']['viewCount']
        like_count = item['statistics']['likeCount']
        
        videos.append({            
            'title': title,
            'url': video_url,
            'views': view_count,
            'likes': like_count            
        })

    return videos

#Create dataframe



#Send Whatsapp message

def send_whatsapp(data):

    text = '\nMost viewed Youtube videos within 24 hours: \n\n ' + str (data[['title', 'video_url', 'views']])
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body = text,
        from_ = "whatsapp:" + PHONE_NUMBER_FROM,
        to = "whatsapp:" + PHONE_NUMBER_TO,
    )

    print(message.body)


