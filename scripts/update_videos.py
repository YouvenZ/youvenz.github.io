"""
scripts/update_videos.py
Pipeline 3 — Fetch all videos from a YouTube channel and update data/videos.yaml.

Usage:
    python scripts/update_videos.py

Required env vars:
    YOUTUBE_API_KEY     — YouTube Data API v3 key
    YOUTUBE_CHANNEL_ID  — Your YouTube channel ID (or set in hugo.yaml)

Optional env vars:
    GH_PAT
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

import requests
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT, deduplicate, git_commit_and_push, load_yaml, log_run, save_yaml

logger = logging.getLogger("update_videos")

VIDEOS_YAML = REPO_ROOT / "data" / "videos.yaml"
YT_API_BASE = "https://www.googleapis.com/youtube/v3"


# ---------------------------------------------------------------------------
# YouTube API helpers
# ---------------------------------------------------------------------------

def _yt_get(endpoint: str, api_key: str, params: dict) -> dict:
    params["key"] = api_key
    resp = requests.get(f"{YT_API_BASE}/{endpoint}", params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_all_videos(api_key: str, channel_id: str) -> list[dict[str, Any]]:
    """Fetch all videos from a channel with pagination."""
    # Get uploads playlist ID
    channel_data = _yt_get("channels", api_key, {
        "id": channel_id,
        "part": "contentDetails",
    })
    items = channel_data.get("items", [])
    if not items:
        logger.error("Channel not found: %s", channel_id)
        return []
    uploads_playlist = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Paginate through all uploads
    video_ids = []
    next_page = None
    while True:
        params: dict = {"playlistId": uploads_playlist, "part": "contentDetails", "maxResults": 50}
        if next_page:
            params["pageToken"] = next_page
        data = _yt_get("playlistItems", api_key, params)
        for item in data.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])
        next_page = data.get("nextPageToken")
        if not next_page:
            break
    logger.info("Found %d video IDs in uploads playlist", len(video_ids))
    return video_ids


def fetch_video_details(api_key: str, video_ids: list[str]) -> list[dict[str, Any]]:
    """Fetch full details for a list of video IDs (50 at a time)."""
    results = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        data = _yt_get("videos", api_key, {
            "id": ",".join(batch),
            "part": "snippet,contentDetails,statistics",
        })
        for item in data.get("items", []):
            snip = item["snippet"]
            stats = item.get("statistics", {})
            duration_raw = item.get("contentDetails", {}).get("duration", "")
            results.append({
                "id": item["id"],
                "title": snip.get("title", ""),
                "description": snip.get("description", "")[:500],
                "publishedAt": snip.get("publishedAt", "")[:10],
                "duration": _parse_duration(duration_raw),
                "viewCount": int(stats.get("viewCount", 0)),
                "likeCount": int(stats.get("likeCount", 0)),
                "thumbnail": (snip.get("thumbnails", {}).get("maxres") or
                              snip.get("thumbnails", {}).get("high") or {}).get("url", ""),
                "tags": snip.get("tags", [])[:10],
                "playlist": None,  # will be filled by playlist fetch
            })
    return results


def fetch_playlists(api_key: str, channel_id: str) -> dict[str, str]:
    """Returns {video_id: playlist_name} mapping."""
    mapping: dict[str, str] = {}
    data = _yt_get("playlists", api_key, {
        "channelId": channel_id,
        "part": "snippet,contentDetails",
        "maxResults": 50,
    })
    for pl in data.get("items", []):
        pl_id = pl["id"]
        pl_name = pl["snippet"]["title"]
        # Fetch playlist items
        next_page = None
        while True:
            params: dict = {"playlistId": pl_id, "part": "contentDetails", "maxResults": 50}
            if next_page:
                params["pageToken"] = next_page
            pl_data = _yt_get("playlistItems", api_key, params)
            for item in pl_data.get("items", []):
                vid_id = item["contentDetails"]["videoId"]
                mapping[vid_id] = pl_name
            next_page = pl_data.get("nextPageToken")
            if not next_page:
                break
    return mapping


def _parse_duration(iso: str) -> str:
    """Convert ISO 8601 duration (PT18M42S) → '18:42'."""
    import re
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not match:
        return ""
    h, m, s = (int(x or 0) for x in match.groups())
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    channel_id = os.environ.get("YOUTUBE_CHANNEL_ID", "")

    if not channel_id:
        hugo_cfg = REPO_ROOT / "hugo.yaml"
        if hugo_cfg.exists():
            cfg = yaml.safe_load(hugo_cfg.read_text())
            channel_id = cfg.get("params", {}).get("youtubeChannelId", "")
    if not api_key or not channel_id:
        logger.error("YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID must be set.")
        sys.exit(1)

    logger.info("Fetching videos for channel %s", channel_id)
    video_ids = fetch_all_videos(api_key, channel_id)
    if not video_ids:
        logger.info("No videos found.")
        log_run("update_videos", 0, 0)
        return

    logger.info("Fetching details for %d videos", len(video_ids))
    new_videos = fetch_video_details(api_key, video_ids)

    logger.info("Fetching playlist metadata")
    try:
        playlist_map = fetch_playlists(api_key, channel_id)
        for v in new_videos:
            v["playlist"] = playlist_map.get(v["id"])
    except Exception as e:
        logger.warning("Playlist fetch failed: %s", e)

    existing = load_yaml(VIDEOS_YAML)
    merged, added, updated = deduplicate(existing, new_videos, key="id")
    merged.sort(key=lambda v: v.get("publishedAt", ""), reverse=True)

    if added == 0 and updated == 0:
        logger.info("No changes detected. Skipping commit.")
        log_run("update_videos", 0, 0)
        return

    save_yaml(VIDEOS_YAML, merged)
    logger.info("Saved %d videos (%d added, %d updated)", len(merged), added, updated)

    log_run("update_videos", added, updated)
    git_commit_and_push(f"auto: update videos ({added} added, {updated} updated)")


if __name__ == "__main__":
    main()
