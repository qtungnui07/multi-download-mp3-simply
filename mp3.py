import os
import platform
import subprocess
import requests
import yt_dlp
import pyperclip  # To monitor clipboard
import re  # To validate URL
import time  # To continuously monitor clipboard
import keyboard  # To detect keyboard shortcuts

# Check and install FFmpeg if not already installed
def check_and_install_ffmpeg():
    ffmpeg_path = "ffmpeg"
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg is already installed.")
    except FileNotFoundError:
        print("FFmpeg not found. Downloading...")
        system = platform.system()
        if system == "Windows":
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        elif system == "Darwin":
            url = "https://evermeet.cx/ffmpeg/ffmpeg.zip"
        elif system == "Linux":
            url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")

        response = requests.get(url, stream=True)
        output_file = "ffmpeg_download.zip"
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("FFmpeg downloaded.")
        
        if system == "Windows":
            import zipfile
            with zipfile.ZipFile(output_file, 'r') as zip_ref:
                zip_ref.extractall("ffmpeg")
            ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
        else:
            import tarfile
            with tarfile.open(output_file, 'r:xz') as tar_ref:
                tar_ref.extractall("ffmpeg")
            ffmpeg_path = os.path.join("ffmpeg", "ffmpeg")
        
        os.environ["PATH"] += os.pathsep + os.path.abspath(os.path.dirname(ffmpeg_path))
        print("FFmpeg has been installed and added to PATH.")

# Download YouTube video as MP3
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

# Check if a URL is a valid YouTube link
def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    )
    return youtube_regex.match(url)

# Monitor clipboard and store valid URLs
def monitor_clipboard_and_store_urls():
    os.makedirs("downloads", exist_ok=True)  # Create downloads folder if it doesn't exist
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
            
            # Check for F8 key press to download all URLs
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

# Main program
if __name__ == "__main__":
    check_and_install_ffmpeg()
    monitor_clipboard_and_store_urls()
