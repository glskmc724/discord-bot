import yt_dlp

opts = {
        'extract-audio': True,
        'format': 'bestaudio',
        'outtmpl': '%(title)s.mp3'
}

def download(link):
    dl = yt_dlp.YoutubeDL(opts)
    res = dl.extract_info(link)
    return dl.prepare_filename(res)
