import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json
from data_sources.reddit_scraper import fetch_reddit_posts

# Download VADER lexicon if not already installed
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER and return a standardized score."""
    sentiment = sia.polarity_scores(text)
    
    # Standardized Score: -1 (negative) to +1 (positive)
    return {
        "text": text,
        "neg": sentiment["neg"],
        "neu": sentiment["neu"],
        "pos": sentiment["pos"],
        "compound": sentiment["compound"],
        "sentiment_score": round(sentiment["compound"], 3)  # Normalized between -1 and 1
    }

def analyze_reddit_sentiment(stock_symbol, method="no_api", count=10):
    """Fetch Reddit posts and analyze their sentiment."""
    posts = fetch_reddit_posts(stock_symbol, method, count)
    
    analyzed_posts = []
    for post in posts:
        sentiment = analyze_sentiment_vader(post["title"])
        analyzed_posts.append({
            "title": post["title"],
            "source": post["source"],
            "sentiment": sentiment["sentiment_score"]
        })
    
    return analyzed_posts

if __name__ == "__main__":
    stock = input("Enter stock symbol (e.g., TSLA, AAPL): ").upper()
    method = input("Choose method (no_api/api): ").strip().lower()
    analyzed_posts = analyze_reddit_sentiment(stock, method, count=10)
    
    if analyzed_posts:
        print(f"Analyzed {len(analyzed_posts)} Reddit posts for sentiment.")
        for post in analyzed_posts:
            print(json.dumps(post, indent=4))