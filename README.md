# Petroleum AI News Daily Digest

Automated daily email digest of AI news related to the petroleum industry, refining, and petrochemicals.

## Features

- Fetches news from Google News RSS and NewsAPI
- Uses Gemini 2.5 Flash AI to filter and rank relevant articles
- Sends daily HTML email digest with top 5 headlines
- Runs automatically via GitHub Actions at 8:00 AM Egypt time

## Tech Stack

| Component | Technology | Cost |
|-----------|------------|------|
| Language | Python 3.11 | Free |
| News Source | Google News RSS + NewsAPI | Free |
| AI Model | Gemini 2.5 Flash | Free |
| Scheduler | GitHub Actions | Free |
| Email | Gmail SMTP | Free |

## Setup Instructions

### 1. Get API Keys

#### Gemini API Key (Required)
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

#### Gmail App Password (Required)
1. Enable 2-Factor Authentication on your Gmail account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Search for "App passwords"
4. Create a new app password for "Mail"
5. Copy the 16-character password

#### NewsAPI Key (Optional)
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key

### 2. Local Testing

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Petroleum_AI_News.git
cd Petroleum_AI_News

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run locally
python -m src.main
```

### 3. Deploy to GitHub

1. Create a new GitHub repository
2. Add secrets in Settings > Secrets and variables > Actions:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `GMAIL_ADDRESS`: Your Gmail address
   - `GMAIL_APP_PASSWORD`: Your Gmail app password
   - `NEWSAPI_KEY`: (Optional) Your NewsAPI key

3. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Petroleum_AI_News.git
git push -u origin main
```

4. The workflow will run automatically at 8:00 AM Egypt time daily

### 4. Manual Trigger

You can manually trigger the workflow from GitHub:
1. Go to Actions tab
2. Select "Daily Petroleum AI News Digest"
3. Click "Run workflow"

## Project Structure

```
Petroleum_AI_News/
├── .github/workflows/
│   └── daily_news.yml      # GitHub Actions scheduler
├── src/
│   ├── __init__.py
│   ├── news_fetcher.py     # Fetches news from RSS/APIs
│   ├── ai_processor.py     # Gemini AI filtering
│   ├── email_sender.py     # Gmail SMTP sender
│   └── main.py             # Main orchestrator
├── config/
│   └── settings.py         # Configuration
├── templates/
│   └── email_template.html # Email HTML template
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Customization

Edit `config/settings.py` to:
- Change search queries
- Modify recipient emails
- Adjust number of headlines

## License

MIT
