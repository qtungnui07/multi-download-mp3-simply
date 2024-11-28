import yt_dlp
from concurrent.futures import ThreadPoolExecutor

def download_youtube_mp3(url, output_path="downloads"):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def multi_download(num_videos):
    urls = []
    for i in range(num_videos):
        url = input(f"URL({i + 1}/{num_videos}): ")
        urls.append(url)
    with ThreadPoolExecutor() as executor:
        print("Download...")
        executor.map(download_youtube_mp3, urls)
    print("Done")
num_videos = int(input("How many music(s) to download: "))
multi_download(num_videos)
