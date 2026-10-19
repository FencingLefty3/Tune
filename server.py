import os

from anyio import Path
from tinytag import TinyTag


musicDir = Path(__file__).parent / "music"
tvDir = Path(__file__).parent / "tv"

def createMusicRecords():

    if not os.path.exists(musicDir):
        return "File not found."

    file_name = os.path.basename(musicDir)
    size_kb = round(os.path.getsize(musicDir) / 1024, 2)

    try:
        tag = TinyTag.get(musicDir)
        length = f"{int(tag.duration // 60)}:{int(tag.duration % 60):02d}" # Format MM:SS
        album = tag.album
        artist = tag.artist
        genre = tag.genre
        track = tag.track
    except Exception:
        length = album = artist = genre = track = "N/A"

    return {
        "file_name": file_name,
        "size_kb": size_kb,
        "length": length,
        "album": album,
        "artist": artist,
        "genre": genre,
        "track": track
    }

def createTVRecords():
   if not os.path.exists(tvDir):
        return "File not found."

    file_name = os.path.basename(tvDir)
    size_kb = round(os.path.getsize(tvDir) / 1024, 2)

    try:
        tag = TinyTag.get(tvDir )
        length = f"{int(tag.duration // 60)}:{int(tag.duration % 60):02d}" # Format MM:SS
        director = tag.director
        year = tag.year
        parental_rating = tag.parental_rating
        genre = tag.genre
        track = tag.track
    except Exception:
        length = director = year = parental_rating = genre = track = "N/A"

    return {
        "file_name": file_name,
        "size_kb": size_kb,
        "length": length,
        "director": director,
        "year": year,
        "parental_rating": parental_rating,
        "genre": genre,
        "track": track
    }