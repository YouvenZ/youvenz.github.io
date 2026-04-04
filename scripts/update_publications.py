"""
scripts/update_publications.py
Pipeline 2 — Fetch and update publications from Google Scholar.

Primary source: Google Scholar via `scholarly` library (Scholar ID: iWgYuY0AAAAJ)
Fallback: arXiv API (when Scholar is blocked or returns no results)

Usage:
    python scripts/update_publications.py

Optional env vars:
    GOOGLE_SCHOLAR_ID   — Override the hardcoded Scholar ID
    UNPAYWALL_EMAIL     — Email for Unpaywall API (OA PDF lookup)
    ARXIV_AUTHOR_NAME   — e.g. "Rachid Zeghlache" (arXiv fallback)
    GH_PAT
"""

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT, deduplicate, git_commit_and_push, load_yaml, log_run, save_yaml, slugify

logger = logging.getLogger("update_publications")

PUBS_YAML = REPO_ROOT / "data" / "publications.yaml"
BIB_FILE = REPO_ROOT / "static" / "publications.bib"
TOPICS_MAP_FILE = Path(__file__).parent / "topics_map.yaml"

GOOGLE_SCHOLAR_ID = "iWgYuY0AAAAJ"  # Rachid Youven Zeghlache

# ---------------------------------------------------------------------------
# Google Scholar via scholarly
# ---------------------------------------------------------------------------

def fetch_google_scholar(scholar_id: str) -> list[dict[str, Any]]:
    """Fetch all publications for a Google Scholar author ID using scholarly."""
    try:
        from scholarly import scholarly as _scholarly
    except ImportError:
        raise ImportError("Install scholarly: pip install scholarly")

    logger.info("Fetching Google Scholar profile for ID: %s", scholar_id)
    author = _scholarly.search_author_id(scholar_id)
    author = _scholarly.fill(author, sections=["basics", "publications"])

    results = []
    pubs = author.get("publications", [])
    logger.info("Found %d publications listed on Scholar", len(pubs))

    for i, pub_stub in enumerate(pubs):
        try:
            pub = _scholarly.fill(pub_stub)
        except Exception as exc:
            logger.warning("Could not fill pub %d: %s", i, exc)
            pub = pub_stub

        bib = pub.get("bib", {})
        title = bib.get("title", "").strip()
        if not title:
            continue

        authors_raw = bib.get("author", "")
        if isinstance(authors_raw, list):
            authors = [{"name": a, "self": False} for a in authors_raw]
        else:
            authors = [{"name": a.strip(), "self": False} for a in authors_raw.split(" and ") if a.strip()]

        year_raw = bib.get("pub_year") or bib.get("year") or ""
        try:
            year = int(str(year_raw)[:4])
        except (ValueError, TypeError):
            year = None

        venue = (bib.get("journal") or bib.get("booktitle") or bib.get("venue") or "").strip()
        abstract = bib.get("abstract", "").strip()
        doi = pub.get("pub_url", "")
        # Extract DOI from URL if it contains doi.org
        if "doi.org/" in doi:
            doi = doi.split("doi.org/")[-1].strip()
        else:
            doi = ""

        eprint = pub.get("eprint_url", "")
        arxiv_url = ""
        if eprint and "arxiv.org" in eprint:
            arxiv_url = eprint

        pdf_url = pub.get("eprint_url", "") if pub.get("eprint_url") else ""

        results.append({
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "type": _infer_type(venue),
            "doi": doi,
            "arxiv": arxiv_url,
            "abstract": abstract,
            "citations": pub.get("num_citations", 0),
            "pdf": pdf_url,
            "tags": [],
        })

        time.sleep(0.5)  # be polite to Scholar

    return results


# ---------------------------------------------------------------------------
# arXiv
# ---------------------------------------------------------------------------

def fetch_arxiv(author_name: str) -> list[dict[str, Any]]:
    query = f"au:{author_name.replace(' ', '+')}"
    url = "https://export.arxiv.org/api/query"
    params = {"search_query": query, "max_results": 50, "sortBy": "submittedDate", "sortOrder": "descending"}
    import xml.etree.ElementTree as ET

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    results = []
    for entry in root.findall("atom:entry", ns):
        arxiv_id = entry.findtext("atom:id", "", ns).split("/abs/")[-1]
        results.append({
            "title": (entry.findtext("atom:title", "", ns) or "").strip(),
            "authors": [
                {"name": a.findtext("atom:name", "", ns), "self": False}
                for a in entry.findall("atom:author", ns)
            ],
            "year": int((entry.findtext("atom:published", "", ns) or "2000")[:4]),
            "venue": "arXiv",
            "type": "preprint",
            "doi": "",
            "arxiv": f"https://arxiv.org/abs/{arxiv_id}",
            "abstract": (entry.findtext("atom:summary", "", ns) or "").strip(),
            "citations": 0,
            "pdf": f"https://arxiv.org/pdf/{arxiv_id}",
            "tags": [],
        })
    return results


# ---------------------------------------------------------------------------
# Unpaywall OA PDF lookup
# ---------------------------------------------------------------------------

def enrich_oa_pdf(doi: str, email: str) -> str:
    if not doi or not email:
        return ""
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            best = data.get("best_oa_location") or {}
            return best.get("url_for_pdf", "")
    except Exception as e:
        logger.debug("Unpaywall lookup failed for %s: %s", doi, e)
    return ""


# ---------------------------------------------------------------------------
# Auto-tagging
# ---------------------------------------------------------------------------

def load_topics_map() -> dict[str, list[str]]:
    if TOPICS_MAP_FILE.exists():
        return yaml.safe_load(TOPICS_MAP_FILE.read_text()) or {}
    return {}


def auto_tag(title: str, abstract: str, topics_map: dict[str, list[str]]) -> list[str]:
    text = (title + " " + abstract).lower()
    tags = []
    for tag, keywords in topics_map.items():
        if any(kw.lower() in text for kw in keywords):
            tags.append(tag)
    return tags


# ---------------------------------------------------------------------------
# BibTeX generation
# ---------------------------------------------------------------------------

def generate_bibtex(pubs: list[dict]) -> str:
    lines = []
    for pub in pubs:
        first_author = (pub.get("authors") or [{}])[0].get("name", "author").split()[-1].lower()
        year = pub.get("year", 2024)
        slug = slugify(pub.get("title", "pub"))[:20].replace("-", "")
        key = f"{first_author}{year}{slug}"
        pub_type = "article" if pub.get("type") == "journal" else "inproceedings" if pub.get("type") == "conference" else "misc"
        lines.append(f"@{pub_type}{{{key},")
        lines.append(f'  title     = {{{pub.get("title", "")}}},')
        authors = " and ".join(a.get("name", "") for a in (pub.get("authors") or []))
        lines.append(f'  author    = {{{authors}}},')
        if pub.get("venue"):
            field = "journal" if pub_type == "article" else "booktitle" if pub_type == "inproceedings" else "howpublished"
            lines.append(f'  {field:<9} = {{{pub["venue"]}}},')
        lines.append(f'  year      = {{{year}}},')
        if pub.get("doi"):
            lines.append(f'  doi       = {{{pub["doi"]}}},')
        if pub.get("arxiv"):
            lines.append(f'  eprint    = {{{pub["arxiv"].split("/")[-1]}}},')
        lines.append("}\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Type inference
# ---------------------------------------------------------------------------

def _infer_type(venue: str) -> str:
    v = venue.lower()
    if any(k in v for k in ["arxiv", "preprint", "biorxiv", "medrxiv"]):
        return "preprint"
    if any(k in v for k in ["conference", "proceedings", "workshop", "icml", "neurips", "iclr", "cvpr"]):
        return "conference"
    if any(k in v for k in ["chapter", "book"]):
        return "book-chapter"
    return "journal"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID", GOOGLE_SCHOLAR_ID)
    unpaywall_email = os.environ.get("UNPAYWALL_EMAIL", "")
    arxiv_author = os.environ.get("ARXIV_AUTHOR_NAME", "")

    new_pubs: list[dict] = []

    logger.info("Fetching from Google Scholar (ID: %s)", scholar_id)
    try:
        new_pubs = fetch_google_scholar(scholar_id)
        logger.info("Google Scholar returned %d papers", len(new_pubs))
    except Exception as e:
        logger.warning("Google Scholar fetch failed: %s", e)

    if not new_pubs and arxiv_author:
        logger.info("Falling back to arXiv for author '%s'", arxiv_author)
        try:
            new_pubs = fetch_arxiv(arxiv_author)
        except Exception as e:
            logger.warning("arXiv fetch failed: %s", e)

    topics_map = load_topics_map()

    # Enrich: OA PDF + auto-tags
    for pub in new_pubs:
        if not pub.get("pdf") and pub.get("doi") and unpaywall_email:
            pub["pdf"] = enrich_oa_pdf(pub["doi"], unpaywall_email)
        if not pub.get("tags"):
            pub["tags"] = auto_tag(pub.get("title", ""), pub.get("abstract", ""), topics_map)
        time.sleep(0.05)  # be polite

    existing = load_yaml(PUBS_YAML)
    merged, added, updated = deduplicate(existing, new_pubs, key="doi" if new_pubs and new_pubs[0].get("doi") else "title")
    merged.sort(key=lambda p: -(p.get("year") or 0))

    if added == 0 and updated == 0:
        logger.info("No changes detected. Skipping commit.")
        log_run("update_publications", 0, 0)
        return

    save_yaml(PUBS_YAML, merged)
    logger.info("Saved %d publications (%d added, %d updated)", len(merged), added, updated)

    # Generate BibTeX
    BIB_FILE.parent.mkdir(parents=True, exist_ok=True)
    BIB_FILE.write_text(generate_bibtex(merged), encoding="utf-8")
    logger.info("Wrote BibTeX to %s", BIB_FILE)

    log_run("update_publications", added, updated)
    git_commit_and_push(f"auto: update publications ({added} added, {updated} updated)")


if __name__ == "__main__":
    main()
