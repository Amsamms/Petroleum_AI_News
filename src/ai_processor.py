import google.generativeai as genai
import json
from typing import List, Dict, Optional

from config.settings import GEMINI_API_KEY, GEMINI_MODEL, TOP_HEADLINES_COUNT


def configure_gemini():
    """Configure the Gemini API client."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment variables.")
    genai.configure(api_key=GEMINI_API_KEY)


def process_news_with_ai(articles: List[Dict]) -> List[Dict]:
    """
    Use Gemini to filter and rank news articles about AI in petroleum industry.
    Returns top 5 most relevant articles with summaries.
    """
    configure_gemini()

    # Prepare articles for the prompt
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"""
Article {i}:
Title: {article['title']}
Source: {article['source']}
Snippet: {article['snippet']}
Link: {article['link']}
---
"""

    prompt = f"""You are an expert in petroleum industry news analysis. Your task is to analyze the following news articles and select the TOP {TOP_HEADLINES_COUNT} most relevant articles about:

1. Artificial Intelligence (AI) applications in the petroleum industry
2. AI in petroleum refining and petrochemical processes
3. Machine learning in oil & gas operations
4. Digital transformation and AI in downstream petroleum

IMPORTANT CRITERIA:
- Articles MUST be specifically about AI/ML/deep learning applications in petroleum/oil/gas/refining/petrochemicals
- Exclude general AI news that doesn't relate to petroleum industry
- Exclude general petroleum news that doesn't involve AI
- Prioritize recent and impactful news
- Prioritize articles about practical implementations over theoretical discussions

For each selected article, provide:
1. The original title
2. A brief 1-2 sentence summary explaining the AI application and its relevance
3. The original link

Respond ONLY with a valid JSON array in this exact format (no markdown, no code blocks, just the JSON):
[
  {{
    "title": "Original article title",
    "summary": "Brief 1-2 sentence summary of the AI application in petroleum context",
    "link": "original article URL",
    "source": "source name"
  }}
]

If fewer than {TOP_HEADLINES_COUNT} articles are relevant, return only the relevant ones.
If NO articles are relevant to AI in petroleum, return an empty array: []

Here are the articles to analyze:

{articles_text}

Remember: Return ONLY the JSON array, no other text."""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        # Parse the response
        response_text = response.text.strip()

        # Clean up the response if it has markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        # Parse JSON
        selected_articles = json.loads(response_text)

        if not isinstance(selected_articles, list):
            print("Warning: AI response was not a list, returning empty results")
            return []

        return selected_articles[:TOP_HEADLINES_COUNT]

    except json.JSONDecodeError as e:
        print(f"Error parsing AI response as JSON: {e}")
        print(f"Raw response: {response.text[:500]}")
        return []
    except Exception as e:
        print(f"Error processing news with AI: {e}")
        return []


if __name__ == "__main__":
    # Test with sample data
    test_articles = [
        {
            "title": "AI Revolutionizes Petroleum Refinery Operations",
            "source": "Oil & Gas Journal",
            "snippet": "Major refineries are adopting AI for predictive maintenance...",
            "link": "https://example.com/1"
        },
        {
            "title": "New ChatGPT Features Released",
            "source": "Tech News",
            "snippet": "OpenAI announces new features for ChatGPT...",
            "link": "https://example.com/2"
        },
        {
            "title": "Machine Learning Optimizes Petrochemical Yields",
            "source": "Chemical Engineering",
            "snippet": "ML algorithms help increase petrochemical production efficiency...",
            "link": "https://example.com/3"
        }
    ]

    results = process_news_with_ai(test_articles)
    print(json.dumps(results, indent=2))
