import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import os

from config.settings import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAILS


def load_email_template() -> str:
    """Load the HTML email template."""
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "templates",
        "email_template.html"
    )
    with open(template_path, "r") as f:
        return f.read()


def format_articles_html(articles: List[Dict]) -> str:
    """Format articles into HTML list items."""
    if not articles:
        return "<p>No relevant AI news in the petroleum industry found today.</p>"

    html = ""
    for i, article in enumerate(articles, 1):
        html += f"""
        <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0;">
            <h3 style="margin: 0 0 8px 0; color: #1a1a1a; font-size: 16px;">
                {i}. {article['title']}
            </h3>
            <p style="margin: 0 0 8px 0; color: #444; font-size: 14px; line-height: 1.5;">
                {article.get('summary', 'No summary available.')}
            </p>
            <a href="{article['link']}" style="color: #0066cc; text-decoration: none; font-size: 14px;">
                Read full article &rarr;
            </a>
            {f'<span style="color: #888; font-size: 12px; margin-left: 10px;">({article.get("source", "Unknown")})</span>' if article.get('source') else ''}
        </div>
        """
    return html


def create_email_content(articles: List[Dict]) -> str:
    """Create the full HTML email content."""
    template = load_email_template()
    today = datetime.now().strftime("%B %d, %Y")
    articles_html = format_articles_html(articles)

    # Replace placeholders in template
    html = template.replace("{{DATE}}", today)
    html = html.replace("{{ARTICLES}}", articles_html)
    html = html.replace("{{ARTICLE_COUNT}}", str(len(articles)))

    return html


def send_email(articles: List[Dict]) -> bool:
    """Send the news digest email to all recipients."""
    if not GMAIL_APP_PASSWORD:
        raise ValueError("GMAIL_APP_PASSWORD is not set. Please set it in your environment variables.")

    today = datetime.now().strftime("%B %d, %Y")
    subject = f"Petroleum AI News Digest - {today}"

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENT_EMAILS)

    # Create HTML content
    html_content = create_email_content(articles)

    # Create plain text version
    plain_text = f"Petroleum AI News Digest - {today}\n\n"
    if articles:
        for i, article in enumerate(articles, 1):
            plain_text += f"{i}. {article['title']}\n"
            plain_text += f"   {article.get('summary', '')}\n"
            plain_text += f"   Link: {article['link']}\n\n"
    else:
        plain_text += "No relevant AI news in the petroleum industry found today.\n"

    # Attach both versions
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        # Connect to Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

            # Send to all recipients
            server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAILS, msg.as_string())

        print(f"Email sent successfully to {len(RECIPIENT_EMAILS)} recipients")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Error: Gmail authentication failed. Check your app password.")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


if __name__ == "__main__":
    # Test with sample data
    test_articles = [
        {
            "title": "AI Revolutionizes Petroleum Refinery Operations",
            "summary": "Major refineries are adopting AI for predictive maintenance and process optimization.",
            "link": "https://example.com/1",
            "source": "Oil & Gas Journal"
        },
        {
            "title": "Machine Learning Optimizes Petrochemical Yields",
            "summary": "ML algorithms help increase petrochemical production efficiency by 15%.",
            "link": "https://example.com/2",
            "source": "Chemical Engineering"
        }
    ]

    # Just print the HTML for testing
    html = create_email_content(test_articles)
    print(html)
