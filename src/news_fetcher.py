import feedparser
import requests
from urllib.parse import quote
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

from config.settings import SEARCH_QUERIES, NEWSAPI_KEY


def fetch_google_news_rss(query: str) -> List[Dict]:
    """Fetch news from Google News RSS feed for a given query."""
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries[:10]:  # Limit to 10 per query
            article = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "source": entry.get("source", {}).get("title", "Unknown"),
                "published": entry.get("published", ""),
                "snippet": entry.get("summary", "")[:200] if entry.get("summary") else ""
            }
            articles.append(article)

        return articles
    except Exception as e:
        print(f"Error fetching Google News RSS for '{query}': {e}")
        return []


def fetch_newsapi(query: str) -> List[Dict]:
    """Fetch news from NewsAPI (if API key is available)."""
    if not NEWSAPI_KEY:
        return []

    url = "https://newsapi.org/v2/everything"

    # Get news from the last 7 days
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    params = {
        "q": query,
        "from": from_date,
        "sortBy": "relevancy",
        "language": "en",
        "pageSize": 10,
        "apiKey": NEWSAPI_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "link": article.get("url", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published": article.get("publishedAt", ""),
                "snippet": article.get("description", "")[:200] if article.get("description") else ""
            })

        return articles
    except Exception as e:
        print(f"Error fetching NewsAPI for '{query}': {e}")
        return []


def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """Remove duplicate articles based on title similarity."""
    seen_titles = set()
    unique_articles = []

    for article in articles:
        # Normalize title for comparison
        title_lower = article["title"].lower().strip()

        # Skip if we've seen a very similar title
        is_duplicate = False
        for seen_title in seen_titles:
            # Simple similarity check - if titles share significant words
            title_words = set(title_lower.split())
            seen_words = set(seen_title.split())
            common_words = title_words & seen_words

            if len(common_words) > min(len(title_words), len(seen_words)) * 0.7:
                is_duplicate = True
                break

        if not is_duplicate and title_lower:
            seen_titles.add(title_lower)
            unique_articles.append(article)

    return unique_articles


def fetch_all_news() -> List[Dict]:
    """Fetch news from all sources and queries, then deduplicate."""
    all_articles = []

    print("Fetching news from Google News RSS...")
    for query in SEARCH_QUERIES:
        articles = fetch_google_news_rss(query)
        all_articles.extend(articles)
        time.sleep(0.5)  # Be nice to the server

    print(f"Fetched {len(all_articles)} articles from Google News RSS")

    # Try NewsAPI if available
    if NEWSAPI_KEY:
        print("Fetching news from NewsAPI...")
        for query in SEARCH_QUERIES[:3]:  # Limit NewsAPI queries to save quota
            articles = fetch_newsapi(query)
            all_articles.extend(articles)
            time.sleep(0.5)
        print(f"Total articles after NewsAPI: {len(all_articles)}")

    # Deduplicate
    unique_articles = deduplicate_articles(all_articles)
    print(f"Unique articles after deduplication: {len(unique_articles)}")

    return unique_articles


if __name__ == "__main__":
    # Test the news fetcher
    articles = fetch_all_news()
    for i, article in enumerate(articles[:10], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Link: {article['link']}")
