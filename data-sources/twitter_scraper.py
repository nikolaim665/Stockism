import tweepy
import os
import json

def load_api_keys():
    """Load Twitter API credentials from environment variables"""
    return {
        "api_key": os.getenv("TWITTER_API_KEY"),
        "api_secret": os.getenv("TWITTER_API_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET")
    }

def authenticate_twitter():
    """Authenticate to Twitter API using Tweepy"""
    keys = load_api_keys()
    auth = tweepy.OAuthHandler(keys["api_key"], keys["api_secret"])
    auth.set_access_token(keys["access_token"], keys["access_secret"])
    return tweepy.API(auth, wait_on_rate_limit=True)

def fetch_tweets(stock_symbol, count=100):
    """Fetch recent tweets mentioning the given stock symbol"""
    api = authenticate_twitter()
    query = f"${stock_symbol} -filter:retweets"
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(count)
    
    tweet_data = []
    for tweet in tweets:
        tweet_data.append({
            "id": tweet.id,
            "text": tweet.full_text,
            "user": tweet.user.screen_name,
            "created_at": tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return tweet_data

def save_tweets_to_json(stock_symbol, tweets):
    """Save tweets to a JSON file"""
    filename = f"{stock_symbol}_tweets.json"
    with open(filename, "w") as f:
        json.dump(tweets, f, indent=4)
    print(f"Saved {len(tweets)} tweets to {filename}")

if __name__ == "__main__":
    stock = input("Enter stock symbol (e.g., TSLA, AAPL): ").upper()
    tweets = fetch_tweets(stock, count=50)
    save_tweets_to_json(stock, tweets)
