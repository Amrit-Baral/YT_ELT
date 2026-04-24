import os
import requests
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv(dotenv_path="./.env")
Api_Key = os.getenv('YT_API_KEY')
maxResults = 50

def get_playlist_id(Channel_Handle=None):

    try:

        if Channel_Handle is None:

            Channel_Handle = "MrBeast"

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_Handle}&key={Api_Key}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        # Code to save Response to file video_stat.json
        # file_path = Path("video_stat.json")
        # file_path.write_text(json.dumps(data, indent=4), encoding='utf-8')

        channel_items = data["items"][0]

        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        # print(channel_playlist_id)
        
        return channel_playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e


def get_video_ids(playlist_id):

    video_ids = []

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={Api_Key}"

    pageToken = None

    try:
        while True:
            url = base_url

            if pageToken:
                url+= f"&pageToken={pageToken}"
            
            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for i in data.get("items", []):
                video_id = i["contentDetails"]["videoId"]
                video_ids.append(video_id)
            
            pageToken = data.get("nextPageToken")

            if not pageToken:
                break
        
        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e


def extract_video_data(video_ids):
    
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for i in range(0, len(video_id_list), batch_size):
            yield video_id_list[i : i + batch_size]
    
    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={Api_Key}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id" : video_id,
                    "title" : snippet["title"],
                    "publishedAt" : snippet["publishedAt"],
                    "duration" : contentDetails["duration"],
                    "viewCount" : statistics.get("viewCount", None),
                    "likeCount" : statistics.get("likeCount", None),
                    "commentCount" : statistics.get("commentCount", None)
                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
