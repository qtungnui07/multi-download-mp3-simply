import os
import platform
import subprocess
import requests
import shutil
import zipfile

def check_and_install_ffmpeg():
    ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg is already installed.")
        return
    except FileNotFoundError:
        print("FFmpeg not found. Downloading...")

    # Determine the system type and download URL
    system = platform.system()
    if system == "Windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    else:
        raise RuntimeError(f"This script currently supports only Windows. Your system: {system}")

    # Download FFmpeg
    response = requests.get(url, stream=True)
    output_file = "ffmpeg_download.zip"
    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("FFmpeg downloaded.")

    # Extract the ZIP file
    extract_path = "ffmpeg_temp"
    with zipfile.ZipFile(output_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Locate the extracted folder
    extracted_folder = next(os.path.join(extract_path, name) for name in os.listdir(extract_path) if os.path.isdir(os.path.join(extract_path, name)))

    # Rename and move to C:\
    final_path = "C:\\ffmpeg"
    if os.path.exists(final_path):
        shutil.rmtree(final_path)
    shutil.move(extracted_folder, final_path)
    print(f"FFmpeg moved to {final_path}.")

    # Add to PATH
    bin_path = os.path.join(final_path, "bin")
    current_path = os.environ.get("PATH", "")
    if bin_path not in current_path:
        os.environ["PATH"] += os.pathsep + bin_path
        subprocess.run(["setx", "PATH", f"%PATH%;{bin_path}"], shell=True)
        print(f"Added {bin_path} to Environment Variables.")
    else:
        print(f"{bin_path} is already in PATH.")

    # Cleanup
    os.remove(output_file)
    shutil.rmtree(extract_path)
    print("Temporary files cleaned up.")

if __name__ == "__main__":
    check_and_install_ffmpeg()
