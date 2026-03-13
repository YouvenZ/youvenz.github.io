#!/usr/bin/env python3
"""
Import Substack/YouTube articles into Hugo blog posts.

For each article listed in articles.md:
  1. Parses the frontmatter
  2. Merges/maps fields to Hugo-compatible format
  3. Creates a simple SVG thumbnail in static/img/thumbnails/
  4. Writes the Hugo post to content/blog/

Usage:
    python scripts/import_articles.py
    python scripts/import_articles.py --dry-run
    python scripts/import_articles.py --overwrite
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HUGO_ROOT = Path(__file__).parent.parent
ARTICLES_MD = HUGO_ROOT / "articles.md"
OUTPUT_DIR = HUGO_ROOT / "content" / "blog"
SVG_DIR = HUGO_ROOT / "static" / "img" / "thumbnails"

# ---------------------------------------------------------------------------
# Cluster → Hugo category mapping
# ---------------------------------------------------------------------------
CLUSTER_CATEGORY_MAP = {
    "📐 AI/ML Concepts": "ai-ml",
    "🖊️ Academic Writing Stack": "academic-writing",
    "🌐 Academic Presence": "academic-presence",
    "⚙️ HPC & Dev Environment": "hpc",
    "🎨 Scientific Visualization": "visualization",
    "🤖 AI for Researchers": "ai-for-researchers",
}

# ---------------------------------------------------------------------------
# Cluster → SVG visual style
# ---------------------------------------------------------------------------
CLUSTER_VISUALS = {
    "📐 AI/ML Concepts":          {"color": "#6366f1", "bg_a": "#1e1b4b", "bg_b": "#0f0f23"},
    "🖊️ Academic Writing Stack":  {"color": "#f59e0b", "bg_a": "#451a03", "bg_b": "#0f0a00"},
    "🌐 Academic Presence":       {"color": "#10b981", "bg_a": "#064e3b", "bg_b": "#011a14"},
    "⚙️ HPC & Dev Environment":   {"color": "#3b82f6", "bg_a": "#1e3a5f", "bg_b": "#050e1c"},
    "🎨 Scientific Visualization": {"color": "#ec4899", "bg_a": "#4a044e", "bg_b": "#130012"},
    "🤖 AI for Researchers":      {"color": "#a78bfa", "bg_a": "#2e1065", "bg_b": "#0a0015"},
}
DEFAULT_VISUAL = {"color": "#8b5cf6", "bg_a": "#1a1a2e", "bg_b": "#0d0d17"}


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_articles_md(filepath: Path) -> list[str]:
    """Extract article file paths from articles.md bullet list."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    # Match Windows paths like: - C:\...\something.md
    return re.findall(r"-\s+(C:\\[^\n]+\.md)", content)


def read_article(filepath: Path):
    """Return (frontmatter_dict, body_str) or (None, None) on failure."""
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
    if not m:
        return None, None
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        print(f"  YAML error in {filepath.name}: {e}")
        return None, None
    return fm, m.group(2).strip()


# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------

def generated_to_date(generated: str) -> str:
    for fmt in ("%Y-%m-%d_%H-%M-%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(generated, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return datetime.now().strftime("%Y-%m-%d")


def cluster_to_category(cluster: str) -> str:
    if cluster in CLUSTER_CATEGORY_MAP:
        return CLUSTER_CATEGORY_MAP[cluster]
    # Strip emoji & normalise
    clean = re.sub(r"[^\w\s/-]", "", cluster).strip().lower()
    return re.sub(r"[\s/]+", "-", clean).strip("-")


def title_to_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug[:60].rstrip("-")


def make_filename(date_str: str, title: str) -> str:
    return f"{date_str}-{title_to_slug(title)}.md"


def build_hugo_frontmatter(fm: dict, svg_hugo_path: str) -> dict:
    """
    Merge original article frontmatter with Hugo blog fields.
    Hugo-specific fields take priority; original metadata is preserved.
    """
    date_str = generated_to_date(fm.get("generated", ""))
    category = cluster_to_category(fm.get("cluster", ""))

    # Null series_part → omit key entirely to keep YAML clean
    series_part = fm.get("series_part")

    hugo_fm: dict = {
        # --- Hugo required ---
        "title": fm.get("title", ""),
        "date": date_str,
        "draft": False,
        # --- Display ---
        "description": fm.get("summary", ""),
        "subtitle": fm.get("subtitle", ""),
        "image": svg_hugo_path,
        # --- Taxonomy ---
        "tags": fm.get("tags", []),
        "categories": [category],
        # --- Series metadata ---
        "is_series": fm.get("is_series", False),
        "article_type": fm.get("article_type", ""),
        # --- Provenance (keep for traceability) ---
        "cluster": fm.get("cluster", ""),
        "critic_score": fm.get("critic_score"),
        "source_transcript": fm.get("source_transcript", ""),
        "generated": fm.get("generated", ""),
    }
    if series_part is not None:
        hugo_fm["series_part"] = series_part

    return hugo_fm, date_str


# ---------------------------------------------------------------------------
# SVG thumbnail generator
# ---------------------------------------------------------------------------

def _wrap_title(title: str, max_len: int = 26) -> tuple[str, str]:
    """Split title into at most two display lines."""
    words = title.split()
    line1, line2 = [], []
    for w in words:
        candidate = " ".join(line1 + [w])
        if len(candidate) <= max_len:
            line1.append(w)
        else:
            line2.append(w)
    l1 = " ".join(line1)
    l2 = " ".join(line2)
    # If line2 is still too long, truncate
    if len(l2) > max_len + 5:
        l2 = l2[: max_len + 2] + "…"
    return l1, l2


def create_svg_thumbnail(title: str, cluster: str, output_path: Path) -> None:
    vis = CLUSTER_VISUALS.get(cluster, DEFAULT_VISUAL)
    color = vis["color"]
    bg_a  = vis["bg_a"]
    bg_b  = vis["bg_b"]

    # Escape XML special chars in text
    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    l1, l2 = _wrap_title(esc(title))
    cluster_label = esc(cluster)
    y_l1 = 175 if not l2 else 158
    y_l2 = y_l1 + 38

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="340" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg_a}"/>
      <stop offset="100%" stop-color="{bg_b}"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{color}"/>
      <stop offset="100%" stop-color="{color}44"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="600" height="340" fill="url(#bgGrad)" rx="10"/>

  <!-- Left accent bar -->
  <rect x="0" y="0" width="5" height="340" fill="url(#barGrad)" rx="2"/>

  <!-- Decorative glow circles -->
  <circle cx="530" cy="50" r="100" fill="{color}" opacity="0.07"/>
  <circle cx="530" cy="50" r="60"  fill="{color}" opacity="0.06"/>
  <circle cx="80"  cy="290" r="70" fill="{color}" opacity="0.05"/>

  <!-- Cluster badge -->
  <rect x="38" y="36" width="280" height="30" rx="6" fill="{color}" opacity="0.15"/>
  <text x="50" y="57"
        font-family="system-ui,-apple-system,'Segoe UI',sans-serif"
        font-size="13" font-weight="600" fill="{color}">{cluster_label}</text>

  <!-- Title -->
  <text x="40" y="{y_l1}"
        font-family="system-ui,-apple-system,'Segoe UI',sans-serif"
        font-size="30" font-weight="700" fill="#ffffff"
        letter-spacing="-0.3">{l1}</text>
  {"" if not l2 else f'<text x="40" y="{y_l2}" font-family="system-ui,-apple-system,\'Segoe UI\',sans-serif" font-size="30" font-weight="700" fill="#ffffff" letter-spacing="-0.3">{l2}</text>'}

  <!-- Bottom stripe -->
  <rect x="0" y="296" width="600" height="44" fill="{color}" opacity="0.12" rx="0"/>
  <rect x="0" y="296" width="600" height="2"  fill="{color}" opacity="0.4"/>
  <text x="50" y="323"
        font-family="system-ui,-apple-system,'Segoe UI',sans-serif"
        font-size="13" fill="{color}" opacity="0.85" font-weight="500">Augmented Scholars</text>
</svg>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Import articles into Hugo blog")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing posts")
    args = parser.parse_args()

    if not ARTICLES_MD.exists():
        sys.exit(f"articles.md not found at {ARTICLES_MD}")

    article_paths = parse_articles_md(ARTICLES_MD)
    print(f"Found {len(article_paths)} articles in articles.md\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)

    created = skipped = errors = 0

    for raw_path in article_paths:
        src = Path(raw_path.strip())
        if not src.exists():
            print(f"  [MISSING]  {src.name}")
            errors += 1
            continue

        fm, body = read_article(src)
        if fm is None:
            print(f"  [ERROR]    {src.name}: could not parse frontmatter")
            errors += 1
            continue

        date_str  = generated_to_date(fm.get("generated", ""))
        title     = fm.get("title", "untitled")
        filename  = make_filename(date_str, title)
        dest      = OUTPUT_DIR / filename

        if dest.exists() and not args.overwrite:
            print(f"  [SKIP]     {filename}  (already exists, use --overwrite)")
            skipped += 1
            continue

        # SVG thumbnail
        svg_name     = filename.replace(".md", ".svg")
        svg_out      = SVG_DIR / svg_name
        svg_hugo_path = f"/img/thumbnails/{svg_name}"

        hugo_fm, _ = build_hugo_frontmatter(fm, svg_hugo_path)

        if args.dry_run:
            print(f"  [DRY-RUN]  would create: {filename}")
            created += 1
            continue

        # Write SVG
        create_svg_thumbnail(title, fm.get("cluster", ""), svg_out)

        # Write Hugo post
        with open(dest, "w", encoding="utf-8") as f:
            f.write("---\n")
            yaml.dump(hugo_fm, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            f.write("---\n\n")
            f.write(body)
            f.write("\n")

        print(f"  [OK]       {filename}")
        created += 1

    print(f"\n{'DRY-RUN ' if args.dry_run else ''}Summary: {created} created, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
