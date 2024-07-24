import os
import googleapiclient.discovery
import pandas as pd
from twilio.rest import Client
from config import YOUTUBE_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER_TO, PHONE_NUMBER_FROM


 # Get videos in the "most popular" category for the past 24 hours

def get_most_watched_videos(region, max_results):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

   
    request = youtube.videos().list(
        part='snippet,statistics',  # Include 'statistics' to get viewCount and likeCount
        chart='mostPopular',
        regionCode=region,
        maxResults=max_results
    )

    response = request.execute()

    # Extract the title, link, viewCount, and likeCount of each video
    videos = []
    num = 1
    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        view_count = item['statistics']['viewCount']
        like_count = item['statistics']['likeCount']
        
        videos.append([num, title, video_url, view_count, like_count])
        num += 1
    
    print (videos)
    return videos

#Create dataframe

def create_dataframe(region, max_results):
    
    col = ['Pos', 'Title', 'Video_url', 'Views', 'Likes']   

    df = pd.DataFrame(get_most_watched_videos(region, max_results), columns=col)
    
    return df.set_index('Pos')


#Send Whatsapp message

def send_whatsapp(data):

    text = '\nMost viewed Youtube videos within 24 hours: \n\n ' + str (data[['Title', 'Video_url', 'Views']])
    
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_ = 'whatsapp:' + PHONE_NUMBER_FROM,
        body = text,
        to = 'whatsapp:' + PHONE_NUMBER_TO
)

    print(message.sid)


