"""
Article History Tracker

Tracks sent articles to prevent the same news from appearing
in multiple daily digests.
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set
from pathlib import Path


# History file location (relative to project root)
HISTORY_FILE = Path(__file__).parent.parent / "data" / "article_history.json"

# Number of days to keep articles in history before cleanup
HISTORY_RETENTION_DAYS = 30


def _normalize_title(title: str) -> str:
    """Normalize title for consistent hashing."""
    # Lowercase, strip whitespace, remove common punctuation
    normalized = title.lower().strip()
    # Remove common variations
    for char in ["'", '"', ":", "-", "—", "|", "..."]:
        normalized = normalized.replace(char, " ")
    # Collapse multiple spaces
    normalized = " ".join(normalized.split())
    return normalized


def _hash_title(title: str) -> str:
    """Create a hash of the normalized title."""
    normalized = _normalize_title(title)
    return hashlib.md5(normalized.encode()).hexdigest()


def _load_history() -> Dict:
    """Load article history from JSON file."""
    if not HISTORY_FILE.exists():
        return {"articles": {}, "last_updated": None}

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load history file: {e}")
        return {"articles": {}, "last_updated": None}


def _save_history(history: Dict) -> None:
    """Save article history to JSON file."""
    # Ensure directory exists
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    history["last_updated"] = datetime.now().isoformat()

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def cleanup_old_entries(history: Dict) -> Dict:
    """Remove entries older than HISTORY_RETENTION_DAYS."""
    cutoff_date = datetime.now() - timedelta(days=HISTORY_RETENTION_DAYS)
    cutoff_str = cutoff_date.isoformat()

    articles = history.get("articles", {})
    cleaned_articles = {
        hash_key: data
        for hash_key, data in articles.items()
        if data.get("date_sent", "") >= cutoff_str
    }

    removed_count = len(articles) - len(cleaned_articles)
    if removed_count > 0:
        print(f"Cleaned up {removed_count} old entries from history")

    history["articles"] = cleaned_articles
    return history


def filter_previously_sent(articles: List[Dict]) -> List[Dict]:
    """
    Filter out articles that have already been sent in previous digests.

    Args:
        articles: List of article dictionaries with 'title' key

    Returns:
        List of articles that haven't been sent before
    """
    history = _load_history()

    # Cleanup old entries first
    history = cleanup_old_entries(history)

    sent_hashes: Set[str] = set(history.get("articles", {}).keys())

    new_articles = []
    skipped_count = 0

    for article in articles:
        title_hash = _hash_title(article.get("title", ""))

        if title_hash in sent_hashes:
            skipped_count += 1
        else:
            new_articles.append(article)

    if skipped_count > 0:
        print(f"Filtered out {skipped_count} previously sent articles")

    # Save cleaned history
    _save_history(history)

    return new_articles


def mark_articles_as_sent(articles: List[Dict]) -> None:
    """
    Mark articles as sent in the history.

    Args:
        articles: List of article dictionaries with 'title' key
    """
    if not articles:
        return

    history = _load_history()

    today = datetime.now().isoformat()

    for article in articles:
        title = article.get("title", "")
        if not title:
            continue

        title_hash = _hash_title(title)

        # Store the hash with metadata
        history.setdefault("articles", {})[title_hash] = {
            "title_preview": title[:80],  # Store truncated title for debugging
            "date_sent": today
        }

    _save_history(history)
    print(f"Marked {len(articles)} articles as sent in history")


def get_history_stats() -> Dict:
    """Get statistics about the article history."""
    history = _load_history()
    articles = history.get("articles", {})

    return {
        "total_tracked": len(articles),
        "last_updated": history.get("last_updated"),
        "retention_days": HISTORY_RETENTION_DAYS
    }


if __name__ == "__main__":
    # Test the history tracker
    stats = get_history_stats()
    print(f"History stats: {stats}")
