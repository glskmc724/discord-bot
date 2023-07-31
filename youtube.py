# https://github.com/JHni2

import yt_dlp
import requests
import iron_token
import json

class Music:
    title = ""
    desc = ""
    thumbnail = ""
    video_id = 0

default_num_search = 1
opts = {
    'extract-audio': True,
    'format': 'bestaudio',
    'outtmpl': '%(title)s.mp3'
}

def search_api(keyword, num_search = default_num_search, youtube_api_key):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": num_search,
        "q": keyword,
        "type": "video",
        "key": youtube_api_key
    }
    resp = requests.get(url, params = params)
    resp.encoding = "utf-8"
    resp_data = resp.json()
    return resp_data


def download(link):
    dl = yt_dlp.YoutubeDL(opts)
    res = dl.extract_info(link)
    return dl.prepare_filename(res)
