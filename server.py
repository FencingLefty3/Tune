import json
import logging
import os
import subprocess
from pathlib import Path
import time
import secrets
import hashlib
import random
import shutil
import sys
import uuid
import math

from datetime import datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote, unquote, urlsplit
from tinytag import TinyTag, TinyTagException

RESOURCE_DIR = Path(
    getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
)
if getattr(sys, "frozen", False):
    DATA_DIR = Path(
        os.environ.get(
            "LOCALAPPDATA",
            Path.home() / "AppData" / "Local",
        )
    ) / "Tune"
else:
    DATA_DIR = Path(__file__).resolve().parent

BASE_DIR = RESOURCE_DIR
MUSIC_DIR = DATA_DIR / "music"
TV_DIR = DATA_DIR / "tv"
MEDIA_DIR = DATA_DIR / "media"


def configure_host_logging():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("tune.host")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(DATA_DIR / "host.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        ))
        logger.addHandler(handler)
        logger.propagate = False
    return logger

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


def runLocalHost():
    print("starting server")
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
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    channels_file = DATA_DIR / "channels.json"
    if not channels_file.exists():
        bundled_channels = RESOURCE_DIR / "channels.json"
        if bundled_channels.is_file():
            shutil.copy2(bundled_channels, channels_file)
        else:
            channels_file.write_text("[]", encoding="utf-8")

    with channels_file.open("r", encoding="utf-8") as file:
        channels = json.load(file)

    return channels

def media_duration_seconds(path):
    try:
        tag = TinyTag.get(str(path))
    except (TinyTagException, OSError) as error:
        raise ValueError(f"Could not read media file: {path}") from error

    duration = tag.duration
    if duration is None or not math.isfinite(duration) or duration <= 0:
        raise ValueError(
            f"Could not determine a valid duration for {path}. "
            "Check the file or use ffprobe for this format."
        )

    return duration

def Create_channel(title, selected_paths, shuffle, media_type):
    title = title.strip()
    if not title:
        raise ValueError("Channel title must not be empty")
    if not selected_paths:
        raise ValueError("Select at least one media file")

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    media = []

    for selected_path in selected_paths:
        source = Path(selected_path).resolve(strict=True)
        duration = media_duration_seconds(source)

        stored = MEDIA_DIR / f"{uuid.uuid4().hex}{source.suffix.lower()}"
        shutil.copy2(source, stored)

        media.append({
            "path": stored.relative_to(DATA_DIR).as_posix(),
            "title": source.stem,
            "duration_seconds": duration,
        })

    channels = Read_chanel()
    if not isinstance(channels, list):
        raise ValueError("channels.json must contain a JSON list of channels")

    channels.append({
        "title": title,
        "media": media,
        "start_at_utc": datetime.now(timezone.utc).isoformat(),
        "shuffle": bool(shuffle),
        "shuffle_seed": secrets.randbits(64),
        "type": media_type,
    })

    with (DATA_DIR / "channels.json").open("w", encoding="utf-8") as file:
        json.dump(channels, file, indent=2)
        
def media_order(channel, cycle_number):
    items = list(channel["media"])

    if not channel.get("shuffle", False):
        return items

    if "shuffle_seed" not in channel:
        raise ValueError(
            f"Channel {channel.get('title', '<untitled>')} "
            "is missing shuffle_seed"
        )

    seed_text = f'{channel["shuffle_seed"]}:{cycle_number}'
    seed = int.from_bytes(
        hashlib.sha256(seed_text.encode("utf-8")).digest()[:8],
        "big",
    )
    random.Random(seed).shuffle(items)
    return items


def scheduled_events(channel, now=None, count=100):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    now = now.astimezone(timezone.utc)

    start = datetime.fromisoformat(
        channel["start_at_utc"].replace("Z", "+00:00")
    )
    if start.tzinfo is None:
        raise ValueError("start_at_utc must include a timezone")
    start = start.astimezone(timezone.utc)

    media = channel["media"]
    if not media:
        return []

    durations = {}
    for item in media:
        duration = float(item["duration_seconds"])
        relative_path = Path(item["path"])

        if (
            not math.isfinite(duration)
            or duration <= 0
            or relative_path.is_absolute()
            or ".." in relative_path.parts
        ):
            raise ValueError(f"Invalid media schedule item: {item}")

        durations[item["path"]] = duration

    cycle_seconds = sum(durations.values())
    if cycle_seconds <= 0:
        raise ValueError("Channel playlist must have a positive duration")

    elapsed = max(0, (now - start).total_seconds())
    cycle_number = int(elapsed // cycle_seconds)
    cycle_position = elapsed - cycle_number * cycle_seconds

    ordered_media = media_order(channel, cycle_number)
    item_index = 0
    item_start_in_cycle = 0.0

    for index, item in enumerate(ordered_media):
        duration = durations[item["path"]]
        if cycle_position < item_start_in_cycle + duration:
            item_index = index
            break
        item_start_in_cycle += duration

    timeline_offset = cycle_number * cycle_seconds + item_start_in_cycle
    events = []

    for _ in range(count):
        item = ordered_media[item_index]
        duration = durations[item["path"]]
        event_start = start + timedelta(seconds=timeline_offset)
        relative_path = Path(item["path"]).as_posix()

        events.append({
            "title": item["title"],
            "media_url": "/" + quote(relative_path, safe="/"),
            "start_at_utc": event_start.isoformat().replace("+00:00", "Z"),
            "duration_seconds": duration,
            "is_current": event_start <= now < event_start + timedelta(
                seconds=duration
            ),
            "offset_seconds": max(0, (now - event_start).total_seconds()),
        })

        timeline_offset += duration
        item_index += 1

        if item_index == len(ordered_media):
            cycle_number += 1
            ordered_media = media_order(channel, cycle_number)
            item_index = 0

    return events

class TuneRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        request_path = urlsplit(path).path
        if request_path == "/media" or request_path.startswith("/media/"):
            relative_path = unquote(request_path[len("/media/"):])
            media_root = MEDIA_DIR.resolve()
            media_path = (media_root / relative_path).resolve()
            try:
                media_path.relative_to(media_root)
            except ValueError:
                return str(media_root / "__invalid_media_path__")
            return str(media_path)
        return super().translate_path(path)

    def log_message(self, format_string, *args):
        logging.getLogger("tune.host").info(
            "%s - %s",
            self.client_address[0],
            format_string % args,
        )

    def do_GET(self):
        if urlsplit(self.path).path != "/api/guide":
            super().do_GET()
            return

        now = datetime.now(timezone.utc)
        channels = Read_chanel()
        payload = {
            "server_now_utc": now.isoformat().replace("+00:00", "Z"),
            "channels": [
                {
                    "title": channel["title"],
                    "events": scheduled_events(channel, now),
                }
                for channel in channels
            ],
        }
        body = json.dumps(payload).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


class TuneHTTPServer(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        logging.getLogger("tune.host").exception(
            "Unhandled HTTP request error from %s",
            client_address[0],
        )


if __name__ == "__main__":
    for r in create_music_records() + create_tv_records():
        print(r)
    for r in create_music_records() + create_tv_records():
        print(r)