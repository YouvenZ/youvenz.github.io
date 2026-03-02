"""
scripts/utils.py — Shared utilities for all automation pipelines.
"""

from __future__ import annotations

import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("utils")

REPO_ROOT = Path(__file__).parent.parent
LOGS_FILE = REPO_ROOT / "logs" / "pipeline_runs.yaml"


# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> list | dict:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def save_yaml(path: Path, data: list | dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Simple slug generator — uses python-slugify if available."""
    try:
        from slugify import slugify as _slugify  # type: ignore
        return _slugify(text)
    except ImportError:
        import re
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        text = re.sub(r"^-+|-+$", "", text)
        return text


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(existing: list[dict], new_items: list[dict], key: str) -> tuple[list[dict], int, int]:
    """
    Merge new_items into existing, keying on *key*.
    Returns (merged_list, added_count, updated_count).
    """
    index: dict[str, dict] = {item[key]: item for item in existing if item.get(key)}
    added, updated = 0, 0
    for item in new_items:
        k = item.get(key)
        if not k:
            continue
        if k not in index:
            index[k] = item
            added += 1
        else:
            # Update mutable fields (e.g. view counts) but preserve manual overrides
            old = index[k]
            changed = False
            for field in ("citations", "viewCount", "likeCount"):
                if field in item and item[field] != old.get(field):
                    old[field] = item[field]
                    changed = True
            if changed:
                updated += 1
    return list(index.values()), added, updated


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git_has_changes() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    return bool(result.stdout.strip())


def git_commit_and_push(message: str) -> None:
    if not git_has_changes():
        logger.info("No changes to commit.")
        return
    cmds = [
        ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
        ["git", "config", "user.name", "github-actions[bot]"],
        ["git", "add", "-A"],
        ["git", "commit", "-m", message],
        ["git", "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Command failed: %s\n%s", " ".join(cmd), result.stderr)
            sys.exit(1)
    logger.info("Committed and pushed: %s", message)


# ---------------------------------------------------------------------------
# Pipeline logging
# ---------------------------------------------------------------------------

def log_run(pipeline: str, added: int = 0, updated: int = 0, errors: list[str] | None = None) -> None:
    LOGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing: list = load_yaml(LOGS_FILE) if LOGS_FILE.exists() else []
    existing.append({
        "pipeline": pipeline,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "added": added,
        "updated": updated,
        "errors": errors or [],
    })
    save_yaml(LOGS_FILE, existing[-200:])  # keep last 200 runs
