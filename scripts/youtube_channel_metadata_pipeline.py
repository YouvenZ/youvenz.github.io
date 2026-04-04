# -*- coding: utf-8 -*-
"""
YouTube Channel Metadata Pipeline
==================================
Fetches metadata for all videos from a YouTube channel, playlist, or
individual video URLs — no audio download, no transcription.

# ── Required packages ─────────────────────────────────────────────────────────
#   pip install yt-dlp pandas
#
# ffmpeg is NOT required for metadata-only extraction.
# ─────────────────────────────────────────────────────────────────────────────
"""

import os
import gc
import pandas as pd
from datetime import datetime
from pathlib import Path

# pip install yt-dlp
try:
    import yt_dlp
except ImportError:
    raise ImportError("Install yt-dlp first:  pip install yt-dlp")

# pip install pandas
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG — edit these values
# ─────────────────────────────────────────────────────────────────────────────

# Paste any combination of:
#   • Individual video URLs  → "https://www.youtube.com/watch?v=VIDEO_ID"
#   • Your channel URL       → "https://www.youtube.com/@YourHandle"
#   • A playlist URL         → "https://www.youtube.com/playlist?list=PL..."
_channel_id = os.environ.get("YOUTUBE_CHANNEL_ID", "")
if _channel_id:
    SOURCES = [f"https://www.youtube.com/channel/{_channel_id}"]
else:
    SOURCES = [
        "https://www.youtube.com/@youvenzful",  # fallback
    ]

# Maximum number of videos to fetch (None = all)
MAX_VIDEOS = None

# Save metadata CSV
SAVE_CSV = True
_script_dir = Path(__file__).resolve().parent
CSV_PATH = str(_script_dir / "youtube_metadata.csv")

# ─────────────────────────────────────────────────────────────────────────────


def make_ydl_opts_metadata_only() -> dict:
    """yt-dlp options: extract info only, no download, no postprocessing."""
    return {
        "quiet": False,
        "no_warnings": False,
        "ignoreerrors": True,
        # Skip the actual download — metadata only
        "skip_download": True,
        "extract_flat": False,
    }


def _flatten_entries(info: dict) -> list:
    """
    Recursively walk yt-dlp's info dict and return a flat list of video dicts.

    yt-dlp represents channels as deeply nested structures:
        channel → tab-playlist → video-playlist → video

    A node is a real video (not a container) when it has no 'entries' key.
    """
    if info is None:
        return []

    entries = info.get("entries")

    # No entries → leaf node (an actual video)
    if entries is None:
        return [info]

    # Has entries → container (channel / tab / playlist) — recurse
    videos = []
    for entry in entries:
        if entry is not None:
            videos.extend(_flatten_entries(entry))
    return videos


def extract_metadata(info: dict) -> dict:
    """Pull the fields we care about from a yt-dlp info dict."""
    video_id = info.get("id", "")

    # Some dates come as "YYYYMMDD" strings
    raw_date = info.get("upload_date", "")
    try:
        upload_date = datetime.strptime(raw_date, "%Y%m%d").date().isoformat()
    except (ValueError, TypeError):
        upload_date = raw_date

    return {
        "video_id":      video_id,
        "title":         info.get("title", ""),
        "channel":       info.get("uploader", ""),
        "channel_id":    info.get("channel_id", ""),
        "upload_date":   upload_date,
        "duration_sec":  info.get("duration"),
        "view_count":    info.get("view_count"),
        "like_count":    info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "description":   (info.get("description") or "")[:500],  # truncated
        "tags":          ", ".join(info.get("tags") or []),
        "url":           info.get("webpage_url", f"https://www.youtube.com/watch?v={video_id}"),
        "fetched_at":    datetime.now().isoformat(timespec="seconds"),
    }


def fetch_channel_metadata(
    sources: list,
    max_videos: int = None,
) -> pd.DataFrame:
    """
    Fetch metadata for all videos in the given sources (no download).

    Parameters
    ----------
    sources    : list of YouTube URLs (videos, channels, or playlists)
    max_videos : cap on the number of videos to process (None = unlimited)

    Returns
    -------
    pd.DataFrame with one row per video
    """
    ydl_opts = make_ydl_opts_metadata_only()
    if max_videos:
        ydl_opts["playlistend"] = max_videos

    records = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for source in sources:
            print(f"\n{'─'*60}")
            print(f"Fetching metadata: {source}")
            print(f"{'─'*60}")

            info_dict = ydl.extract_info(source, download=False)

            if info_dict is None:
                print(f"  [!] Could not extract info for: {source}")
                continue

            videos = _flatten_entries(info_dict)
            print(f"  Found {len(videos)} video(s)")

            for info in videos:
                try:
                    meta = extract_metadata(info)
                    print(f"  [✓] {meta['title'][:70]}")
                    records.append(meta)
                except Exception as exc:
                    print(f"  [!] Error processing video {info.get('id')}: {exc}")

    df = pd.DataFrame(records)

    col_order = [
        "video_id", "title", "channel", "upload_date", "duration_sec",
        "view_count", "like_count", "comment_count",
        "url", "tags", "description", "channel_id", "fetched_at",
    ]
    df = df[[c for c in col_order if c in df.columns]]

    return df


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("YouTube Channel Metadata Fetcher")
    print("=" * 60)
    print(f"Sources : {len(SOURCES)} source(s)")

    df = fetch_channel_metadata(sources=SOURCES, max_videos=MAX_VIDEOS)

    print(f"\n{'='*60}")
    print(f"Done. {len(df)} video(s) found.")

    if SAVE_CSV and not df.empty:
        df.to_csv(CSV_PATH, index=False)
        print(f"Metadata saved → {CSV_PATH}")

    return df


if __name__ == "__main__":
    df = main()
