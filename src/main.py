#!/usr/bin/env python3
"""
Petroleum AI News Daily Digest

This script fetches AI-related news in the petroleum industry,
processes them with Gemini AI, and sends a daily email digest.
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.news_fetcher import fetch_all_news
from src.ai_processor import process_news_with_ai
from src.email_sender import send_email
from src.history_tracker import filter_previously_sent, mark_articles_as_sent, get_history_stats


def main():
    """Main function to orchestrate the news digest pipeline."""
    print("=" * 60)
    print(f"Petroleum AI News Digest - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Show history stats
    stats = get_history_stats()
    print(f"History: {stats['total_tracked']} articles tracked (retention: {stats['retention_days']} days)")

    # Step 1: Fetch news from all sources
    print("\n[1/4] Fetching news articles...")
    articles = fetch_all_news()

    if not articles:
        print("Warning: No articles fetched. Check your internet connection.")
        # Still send email to notify about the issue
        send_email([])
        return

    print(f"Fetched {len(articles)} unique articles")

    # Step 1b: Filter out previously sent articles
    print("\n[2/4] Filtering previously sent articles...")
    articles = filter_previously_sent(articles)

    if not articles:
        print("Warning: All fetched articles were previously sent. No new news today.")
        return

    print(f"Remaining new articles: {len(articles)}")

    # Step 3: Process with AI to filter and rank
    print("\n[3/4] Processing articles with Gemini AI...")
    processed_articles = process_news_with_ai(articles)

    if not processed_articles:
        print("Warning: No relevant articles found after AI processing.")

    print(f"Selected {len(processed_articles)} relevant articles")

    # Print selected articles
    for i, article in enumerate(processed_articles, 1):
        print(f"\n  {i}. {article['title']}")
        print(f"     Summary: {article.get('summary', 'N/A')[:100]}...")

    # Step 4: Send email
    print("\n[4/4] Sending email digest...")
    success = send_email(processed_articles)

    if success:
        print("\nEmail sent successfully!")
        # Mark articles as sent in history (only after successful send)
        mark_articles_as_sent(processed_articles)
    else:
        print("\nFailed to send email. Check your configuration.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
