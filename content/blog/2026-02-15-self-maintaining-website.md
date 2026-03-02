---
title: "From YouTube to Blog Post: How I Built a Self-Maintaining Website"
date: 2026-02-15
tags: ["hugo", "automation", "python", "github-actions"]
categories: ["tutorial"]
description: "A walkthrough of the GitHub Actions pipeline that automatically converts my YouTube videos into blog posts using Claude AI."
image: ""
draft: false
---

In this post I walk through the three automation pipelines that keep this website up to date without any manual intervention.

## TL;DR

- A daily GitHub Actions cron job fetches my latest YouTube video
- Downloads the transcript using `youtube-transcript-api`
- Sends it to Claude (`claude-sonnet-4-20250514`) to generate a structured blog post
- Commits the Markdown file and triggers a Hugo rebuild

## Key Takeaways

1. The whole process takes about 60 seconds from video publish to draft post
2. The Claude prompt is the most important part — iteration matters
3. Always diff before commit to avoid unnecessary rebuilds

## The Pipeline

### Step 1: Detect new video

```python
import yaml, requests

def get_latest_video(api_key, channel_id):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {"key": api_key, "channelId": channel_id,
              "order": "date", "part": "snippet", "maxResults": 1}
    r = requests.get(url, params=params).json()
    return r["items"][0]
```

### Step 2: Generate blog post with Claude

The Claude API call uses a structured prompt that ensures the output
includes all required frontmatter fields and a consistent article structure.

{{< youtube id="dQw4w9WgXcQ" title="Example video" >}}

## Conclusion

The combination of Hugo's speed, GitHub Actions' reliability, and Claude's
writing ability creates a surprisingly capable content pipeline.
