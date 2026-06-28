import sys
import subprocess
import tempfile
from pathlib import Path

import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError

# Basis-Ordner: neben der .exe bzw. neben der .py
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

TEMP_DIR = Path(tempfile.gettempdir()) / 'music_downloader_temp'
CONFIG_FILE = BASE_DIR / 'config.txt'
DEFAULT_DOWNLOAD_DIR = BASE_DIR / 'download'

DEFAULT_DOWNLOAD_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)


def load_download_dir():
    if CONFIG_FILE.exists():
        saved = CONFIG_FILE.read_text().strip()
        if saved and Path(saved).exists():
            return Path(saved)
    return DEFAULT_DOWNLOAD_DIR


def save_download_dir(path):
    CONFIG_FILE.write_text(str(path))


def download(url, progress_callback=None, download_dir=None):
    output_dir = Path(download_dir) if download_dir else DEFAULT_DOWNLOAD_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    def progress_hook(d):
        if not progress_callback:
            return
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '?%').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            progress_callback(f"⬇ {percent}  –  {speed}  –  ETA {eta}")
        elif d['status'] == 'finished':
            progress_callback("🔄 Konvertiere zu MP3...")

    ydl_opts = {
        'outtmpl': str(TEMP_DIR / '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'progress_hooks': [progress_hook],
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                'key': 'EmbedThumbnail',
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'unknown')
            temp_mp3 = TEMP_DIR / f"{title}.mp3"
            final_mp3 = output_dir / f"{title}.mp3"

            if progress_callback:
                progress_callback("🔧 Finalisiere Datei...")

            subprocess.run([
                'ffmpeg', '-y',
                '-i', str(temp_mp3),
                '-c:a', 'libmp3lame',
                '-b:a', '192k',
                '-id3v2_version', '3',
                str(final_mp3)
            ], check=True, capture_output=True)

            temp_mp3.unlink(missing_ok=True)

            if progress_callback:
                progress_callback(f"✅ Fertig: {title}.mp3")

    except DownloadError as e:
        if progress_callback:
            progress_callback(f"❌ Download fehlgeschlagen: {e}")
        print(f"Download failed: {e}")
    except ExtractorError as e:
        if progress_callback:
            progress_callback(f"❌ Fehler: {e}")
        print(f"Extraction failed: {e}")
    except subprocess.CalledProcessError as e:
        if progress_callback:
            progress_callback("❌ FFmpeg Fehler beim Finalisieren")
        print(f"FFmpeg failed: {e}")


if __name__ == "__main__":
    download(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        progress_callback=print
    )