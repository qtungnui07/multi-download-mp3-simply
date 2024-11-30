import os
import platform
import subprocess
import requests

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
