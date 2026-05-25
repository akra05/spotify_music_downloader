import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from pathlib import Path

#define directory
BASE_DIR = Path(__file__).parent
DOWNLOAD_DIR = BASE_DIR / 'download'
DIR_AS_STR = str(DOWNLOAD_DIR)

DOWNLOAD_DIR.mkdir(exist_ok=True)

#function for downloading
def download(url):
    ydl_opts = {
        'outtmpl': f'{DIR_AS_STR}/%(title)s.%(ext)s',
        "writethumbnail": True,
        'postprocessors': [
            {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            },
            {
                'key': 'EmbedThumbnail',
            }],

        'playlistend': None,
        'write_playlist_metafiles': False 
    }


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.download([url])
            print(info)
    except DownloadError as e:
        print(f"Download failed: {e}")
    except ExtractorError as e:
        print(f"Extraction failed: {e}")



if __name__ == "__main__":
    download()
