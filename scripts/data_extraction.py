import os
import json
import tweepy
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
# Loading Twitter API credentials from environment variables

def authenticate_twitter():
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthUserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def extract_tweets(search_query, count=10):
    """Extract tweets based on search query"""
    api = authenticate_twitter()
    
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, 
                               q=search_query, 
                               lang="en", 
                               tweet_mode="extended").items(count):
        tweet_data = {
            'id': tweet.id_str,
            'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'text': tweet.full_text,
            'user_name': tweet.user.screen_name,
            'user_location': tweet.user.location,
            'retweet_count': tweet.retweet_count,
            'favorite_count': tweet.favorite_count,
            'hashtags': [hashtag['text'] for hashtag in tweet.entities['hashtags']],
            'search_query': search_query
        }
        tweets.append(tweet_data)
    
    return pd.DataFrame(tweets)

def save_tweets(df, output_path):
    """Save tweets to CSV file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_path}/tweets_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} tweets to {filename}")
    return filename

if __name__ == "__main__":
    # Example usage
    search_terms = ["climate change", "renewable energy", "sustainability"]
    
    all_tweets = pd.DataFrame()
    for term in search_terms:
        print(f"Extracting tweets for: {term}")
        tweets_df = extract_tweets(term, count=200)
        all_tweets = pd.concat([all_tweets, tweets_df])
    
    save_tweets(all_tweets, "data/raw")