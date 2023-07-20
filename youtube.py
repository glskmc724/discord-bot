# https://github.com/JHni2

from selenium import webdriver as wb
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import yt_dlp
import requests
import json
import iron_token

default_num_search = 1
opts = {
        'extract-audio': True,
        'format': 'bestaudio',
        'outtmpl': '%(title)s.mp3'
}


def search(keyword, num_search = default_num_search):
    caps = DesiredCapabilities.CHROME
    caps["pageLoadStrategy"] = "none"
    opts = wb.ChromeOptions()
    opts.add_argument("headless")

    driver = wb.Chrome(options=opts)
    url = f'https://www.youtube.com/results?search_query={keyword}'
    driver.get(url)
    #body = driver.find_element(By.TAG_NAME,'body')
    #body.send_keys(Keys.PAGE_DOWN)

    #for i in range(1,51):
    #    body.send_keys(Keys.PAGE_DOWN)
    #    time.sleep(0.5)

    soup = bs(driver.page_source, 'lxml')

    res = []

    # 영상 썸네일
    thumbnail = soup.select('#thumbnail > yt-image > img') 
    for idx, val in enumerate(thumbnail[:num_search]):
        if 'src' in val.attrs:
            if idx >= len(res):
                res.append({
                    'thumbnail': val.attrs['src'],
                    'title': '',
                    'href': '',
                })
            else:
                # 이미 존재하는 딕셔너리 업데이트
                res[idx].update({
                    'thumbnail': val.attrs['src'],
                })
    
    # 영상 제목, 링크 
    title = soup.select('a#video-title')
    for idx, val in enumerate(title[:num_search]):
        if idx >= len(res):
            res.append({
                'title': val.text.strip(),
                'href': 'https://www.youtube.com' + val.attrs['href'],
            })
        else:
        # 이미 존재하는 딕셔너리 업데이트
            res[idx].update({
                'title': val.text.strip(),
                'href': 'https://www.youtube.com' + val.attrs['href'],
            })

    return res;

def search_api(keyword, num_search = default_num_search):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": default_num_search,
        "q": keyword,
        "type": "video",
        "key": iron_token.YOUTUBE_API_KEY
    }
    resp = requests.get(url, params = params)
    resp.encoding = "utf-8"
    resp_data = resp.json()
    return resp_data


def download(link):
    dl = yt_dlp.YoutubeDL(opts)
    res = dl.extract_info(link)
    return dl.prepare_filename(res)
