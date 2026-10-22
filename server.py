import json
import subprocess
from pathlib import Path
import time

from tinytag import TinyTag, TinyTagException

BASE_DIR = Path(__file__).parent
MUSIC_DIR = BASE_DIR / "music"
TV_DIR = BASE_DIR / "tv"

import socket

def get_local_ipv4():  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

localHost = subprocess.Popen(["python", "-m", "http.server"])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down server...")
    localHost.terminate()
    localHost.wait()
    print("Server stopped.")


def format_length(seconds):
    """Seconds -> 'M:SS', or None if the duration is unknown."""
    if seconds is None:
        return None
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}:{secs:02d}"


def read_tag(path):
    """Returns a TinyTag, or None if the file can't be read."""
    try:
        return TinyTag.get(path)
    except (TinyTagException, OSError):
        return None


def base_record(path, tag):
    return {
        "file_name": path.name,
        "path": str(path),
        "size_kb": round(path.stat().st_size / 1024, 2),
        "length": format_length(tag.duration) if tag else None,
        "genre": tag.genre if tag else None,
    }


def media_files(folder):
    """Every supported file under folder (including sub-folders), sorted."""
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*")
                  if p.is_file() and TinyTag.is_supported(str(p)))


def create_music_records():
    records = []
    for path in media_files(MUSIC_DIR):
        tag = read_tag(path)
        records.append({
            **base_record(path, tag),
            "title": tag.title if tag else None,
            "album": tag.album if tag else None,
            "artist": tag.artist if tag else None,
            "track": tag.track if tag else None,
        })
    return records


def create_tv_records():
    records = []
    for path in media_files(TV_DIR):
        tag = read_tag(path)
        records.append({
            **base_record(path, tag),
            "title": (tag.title if tag and tag.title else path.stem),
            "year": tag.year if tag else None,
           
        })
    return records

def Read_chanel():

    with open(BASE_DIR / "channels.json", "r") as file:
        channels = json.load(file)

    return channels

def Create_channel(title, media_ids, shuffle, type):
    if not media_ids:
        raise ValueError("media_ids must not be empty")
    try:
        with open(BASE_DIR / "channels.json", "r") as file:
            channels = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        channels = []

    if channels == {}:
        channels = []
    if not isinstance(channels, list):
        raise ValueError("channels.json must contain a JSON list of channels")

    new_channel = {
        "title": title,
        "media_ids": media_ids,
        "shuffle": shuffle,
        "type": type
    }
    channels.append(new_channel)

    with open(BASE_DIR / "channels.json", "w") as file:
        json.dump(channels, file, indent=2)




if __name__ == "__main__":
    for r in create_music_records() + create_tv_records():
        print(r)

Read_chanel()