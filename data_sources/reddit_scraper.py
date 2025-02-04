import requests
import praw
from bs4 import BeautifulSoup
import os
import json

def fetch_reddit_no_api(stock_symbol, subreddit="stocks", count=10):
    """Fetch Reddit posts without an API key using BeautifulSoup."""
    url = f"https://www.reddit.com/r/{subreddit}/search?q={stock_symbol}&restrict_sr=1&sort=new"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch Reddit posts (no API)")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    posts = []
    
    for post in soup.find_all("div", class_="Post")[:count]:
        title = post.find("h3")
        if title:
            posts.append({
                "title": title.text.strip(),
                "source": "Reddit (Scraped)",
            })
    
    return posts

def fetch_reddit_with_api(stock_symbol, subreddit="stocks", count=10):
    """Fetch Reddit posts using the official API (praw)."""
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    
    posts = []
    subreddit = reddit.subreddit(subreddit)
    
    for submission in subreddit.search(stock_symbol, sort="new", limit=count):
        posts.append({
            "title": submission.title,
            "source": "Reddit (API)",
        })
    
    return posts

def fetch_reddit_posts(stock_symbol, method="no_api", count=10):
    """Fetch Reddit posts using the specified method."""
    if method == "no_api":
        return fetch_reddit_no_api(stock_symbol, count=count)
    elif method == "api":
        return fetch_reddit_with_api(stock_symbol, count=count)
    else:
        print("Invalid method specified. Use 'no_api' or 'api'.")
        return []

if __name__ == "__main__":
    stock = input("Enter stock symbol (e.g., TSLA, AAPL): ").upper()
    method = input("Choose method (no_api/api): ").strip().lower()
    posts = fetch_reddit_posts(stock, method, count=10)
    
    if posts:
        print(f"Fetched {len(posts)} Reddit posts using {method}.")
        for post in posts:
            print(post)
