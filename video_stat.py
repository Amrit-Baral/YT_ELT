import os
import requests
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv(dotenv_path="./.env")
Api_Key = os.getenv('YT_API_KEY')


def get_playlist_id(Channel_Handle=None):

    try:

        if Channel_Handle is None:

            Channel_Handle = "MrBeast"

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_Handle}&key={Api_Key}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        file_path = Path("video_stat.json")

        file_path.write_text(json.dumps(data, indent=4), encoding='utf-8')

        channel_items = data["items"][0]

        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        # print(channel_playlist_id)
        
        return channel_playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    get_playlist_id()
