from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pathlib import Path
import sys

def inspect(filepath: str):
    path = Path(filepath)
    if not path.exists():
        print(f"Datei nicht gefunden: {filepath}")
        return

    print(f"\n{'='*60}")
    print(f"Datei: {path.name}")
    print(f"Größe: {path.stat().st_size / 1024:.1f} KB")
    print(f"{'='*60}")

    # MP3-Infos
    try:
        audio = MP3(filepath)
        print(f"Länge:    {audio.info.length:.1f}s")
        print(f"Bitrate:  {audio.info.bitrate // 1000} kbps")
        print(f"Channels: {audio.info.channels}")
        print(f"Sample:   {audio.info.sample_rate} Hz")
    except Exception as e:
        print(f"⚠ MP3-Fehler: {e}")

    # ID3-Tags
    print(f"\n--- ID3 Tags ---")
    try:
        tags = ID3(filepath)
        if not tags:
            print("(keine Tags vorhanden)")
        for key, val in sorted(tags.items()):
            # Cover nicht ausschreiben
            if key.startswith('APIC'):
                print(f"  {key}: [Cover eingebettet, {len(val.data)} bytes]")
            else:
                print(f"  {key}: {val}")
    except Exception as e:
        print(f"⚠ Tag-Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect(sys.argv[1])
    else:
        # Alle MP3s im download-Ordner anzeigen
        folder = Path(__file__).parent / 'download'
        mp3s = list(folder.glob('*.mp3'))
        if not mp3s:
            print("Keine MP3s im download-Ordner gefunden.")
        for f in mp3s:
            inspect(str(f))