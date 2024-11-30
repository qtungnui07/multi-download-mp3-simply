
import importlib
import subprocess
import sys

def install_and_import(package):
    """
    Kiểm tra nếu module, thiếu thì auto install
    """
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Module {package} chưa được cài đặt. Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)
required_modules = ["requests", "yt_dlp", "pyperclip", "keyboard"]
for module in required_modules:
    install_and_import(module)
from modules.ffmpeg import check_and_install_ffmpeg
from modules.youtube import monitor_clipboard_and_store_urls

if __name__ == "__main__":
    check_and_install_ffmpeg()
    monitor_clipboard_and_store_urls()
