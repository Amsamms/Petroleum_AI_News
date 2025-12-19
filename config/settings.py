import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # Optional

# Email Configuration
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "ahmedsabri85@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAILS = [
    "asabri@eprom-midor.com.eg",
    "ahmedsabri85@gmail.com"
]

# News Search Configuration
SEARCH_QUERIES = [
    "AI petroleum industry",
    "artificial intelligence oil gas",
    "AI petroleum refining",
    "AI petrochemicals",
    "machine learning oil refinery",
    "deep learning petroleum",
    "AI downstream oil",
    "artificial intelligence refinery optimization"
]

# Number of top headlines to include
TOP_HEADLINES_COUNT = 5

# Gemini Model
GEMINI_MODEL = "gemini-2.5-flash"
