import os
import platform
import subprocess
import requests
import yt_dlp
from concurrent.futures import ThreadPoolExecutor


def check_and_install_ffmpeg():
    ffmpeg_path = "ffmpeg" 
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg đã được cài đặt.")
    except FileNotFoundError:
        print("FFmpeg chưa được cài đặt. Bắt đầu tải...")
        system = platform.system()
        if system == "Windows":
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        elif system == "Darwin":
            url = "https://evermeet.cx/ffmpeg/ffmpeg.zip"
        elif system == "Linux":
            url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        else:
            raise RuntimeError(f"Hệ điều hành {system} không được hỗ trợ.")
        response = requests.get(url, stream=True)
        output_file = "ffmpeg_download.zip"
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Tải xong FFmpeg.")
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
        print("FFmpeg đã được cài đặt và thêm vào PATH.")
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

if __name__ == "__main__":
    check_and_install_ffmpeg()
    num_videos = int(input("How many music(s) to download: "))
    multi_download(num_videos)
