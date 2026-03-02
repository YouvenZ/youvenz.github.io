"""
scripts/video_to_blog.py
Pipeline 1 — Convert latest YouTube video into a Hugo blog post via Claude.

Usage:
    python scripts/video_to_blog.py

Required env vars:
    YOUTUBE_API_KEY   — YouTube Data API v3 key
    ANTHROPIC_API_KEY — Anthropic API key
    YOUTUBE_CHANNEL_ID — Your YouTube channel ID

Optional env vars:
    GH_PAT — used by git push (set in Actions via secrets)
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT, load_yaml, save_yaml, slugify, git_commit_and_push, log_run

logger = logging.getLogger("video_to_blog")

VIDEOS_YAML = REPO_ROOT / "data" / "videos.yaml"
BLOG_DIR = REPO_ROOT / "content" / "blog"

# ---------------------------------------------------------------------------
# YouTube helpers
# ---------------------------------------------------------------------------

def fetch_latest_video(api_key: str, channel_id: str) -> dict[str, Any] | None:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": api_key,
        "channelId": channel_id,
        "order": "date",
        "part": "snippet",
        "maxResults": 1,
        "type": "video",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        return None
    item = items[0]
    return {
        "id": item["id"]["videoId"],
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "publishedAt": item["snippet"]["publishedAt"][:10],
        "thumbnail": f"https://img.youtube.com/vi/{item['id']['videoId']}/maxresdefault.jpg",
        "tags": item["snippet"].get("tags", []),
    }


def fetch_transcript(video_id: str) -> str:
    """Try youtube-transcript-api; fall back to empty string."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(t["text"] for t in transcript)
    except Exception as e:
        logger.warning("Could not fetch transcript for %s: %s", video_id, e)
        return ""


def is_already_processed(video_id: str) -> bool:
    """Check if a blog post for this video ID already exists."""
    for md in BLOG_DIR.glob("*.md"):
        content = md.read_text(encoding="utf-8")
        if f"youtube_id: {video_id}" in content:
            return True
    return False


# ---------------------------------------------------------------------------
# Claude API
# ---------------------------------------------------------------------------

def generate_blog_post(
    api_key: str,
    title: str,
    transcript: str,
    description: str,
    tags: list[str],
    date: str,
    video_id: str,
) -> str:
    import anthropic  # type: ignore

    client = anthropic.Anthropic(api_key=api_key)

    content_source = transcript[:6000] if transcript else description[:2000]
    system_prompt = (
        "You are an expert technical writer creating blog posts for an academic researcher's website. "
        "Write in a clear, accessible yet rigorous style. "
        "Output ONLY the Markdown content — no preamble, no explanation."
    )
    user_prompt = f"""
Create a complete Hugo blog post for the following YouTube video.

Video title: {title}
Video ID: {video_id}
Publish date: {date}
Tags: {', '.join(tags)}
Content (transcript or description):
{content_source}

Requirements:
1. Begin with YAML frontmatter (title, date, tags, categories, description, youtube_id, draft: false)
2. Include sections: TL;DR, Key Takeaways (bullet list), full write-up (3–5 paragraphs), embedded video using {{{{< youtube id="{video_id}" >}}}}, and a canonical note at the bottom
3. Use Markdown headings (##), code blocks where relevant
4. Keep the tone academic but accessible
5. Return ONLY the Markdown, starting with ---
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": user_prompt}],
        system=system_prompt,
    )
    return message.content[0].text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    api_key = os.environ["YOUTUBE_API_KEY"]
    anthropic_key = os.environ["ANTHROPIC_API_KEY"]
    channel_id = os.environ.get("YOUTUBE_CHANNEL_ID", "")

    if not channel_id:
        # Try to read from hugo.yaml
        hugo_cfg = REPO_ROOT / "hugo.yaml"
        if hugo_cfg.exists():
            cfg = yaml.safe_load(hugo_cfg.read_text())
            channel_id = cfg.get("params", {}).get("youtubeChannelId", "")
    if not channel_id:
        logger.error("YOUTUBE_CHANNEL_ID not set and not found in hugo.yaml")
        sys.exit(1)

    logger.info("Fetching latest video from channel %s", channel_id)
    video = fetch_latest_video(api_key, channel_id)
    if not video:
        logger.info("No videos found.")
        log_run("video_to_blog", 0, 0)
        return

    logger.info("Latest video: %s (%s)", video["title"], video["id"])

    if is_already_processed(video["id"]):
        logger.info("Blog post already exists for video %s. Skipping.", video["id"])
        log_run("video_to_blog", 0, 0)
        return

    transcript = fetch_transcript(video["id"])
    post_md = generate_blog_post(
        api_key=anthropic_key,
        title=video["title"],
        transcript=transcript,
        description=video["description"],
        tags=video.get("tags", [])[:8],
        date=video["publishedAt"],
        video_id=video["id"],
    )

    slug = slugify(video["title"])
    filename = f"{video['publishedAt']}-{slug}.md"
    output_path = BLOG_DIR / filename
    output_path.write_text(post_md, encoding="utf-8")
    logger.info("Saved blog post: %s", output_path)

    log_run("video_to_blog", 1, 0)
    git_commit_and_push(f"auto: blog post from video '{video['title'][:60]}'")


if __name__ == "__main__":
    main()
