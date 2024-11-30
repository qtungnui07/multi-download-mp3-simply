import os
import re
import time
import pyperclip
import keyboard
from yt_dlp import YoutubeDL

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

    os.makedirs(output_path, exist_ok=True)
    with YoutubeDL(options) as ydl:
        ydl.download([url])

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    )
    return youtube_regex.match(url)

def monitor_clipboard_and_store_urls():
    stored_urls = [] 
    previous_clipboard = ""

    print("Monitoring clipboard... Copy YouTube URLs and press F8 to download all.")

    while True:
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != previous_clipboard:
                previous_clipboard = current_clipboard
                if is_valid_youtube_url(current_clipboard):
                    if current_clipboard not in stored_urls:
                        stored_urls.append(current_clipboard)
                        print(f"URL added to list: {current_clipboard}")

            if keyboard.is_pressed("f8"):
                if stored_urls:
                    print("Downloading all URLs...")
                    for url in stored_urls:
                        print(f"Downloading: {url}")
                        download_youtube_mp3(url)
                    print("All downloads completed!")
                    stored_urls.clear()
                else:
                    print("No URLs to download.")
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.5)
