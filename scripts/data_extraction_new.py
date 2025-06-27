import os
import json
import tweepy
import pandas as pd
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def authenticate_twitter():
    """Authenticate with Twitter API v2 using bearer token"""
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not bearer_token:
        raise ValueError("Twitter API bearer token is missing. Please set TWITTER_BEARER_TOKEN in your environment variables.")
    
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    return client

def extract_tweets(search_query, count=10):
    """Extract tweets based on search query using Twitter API v2 if available, otherwise fall back to mock data"""
    try:
        client = authenticate_twitter()
        
        response = client.search_recent_tweets(
            query=search_query,
            max_results=min(count, 100),
            tweet_fields=['created_at', 'public_metrics', 'entities']
        )
        
        if response.data:
            tweets = []
            for tweet in response.data:
                hashtags = []
                if hasattr(tweet, 'entities') and tweet.entities and 'hashtags' in tweet.entities:
                    hashtags = [tag['tag'] for tag in tweet.entities['hashtags']]
                
                metrics = tweet.public_metrics if hasattr(tweet, 'public_metrics') else {}
                
                tweet_data = {
                    'id': str(tweet.id),
                    'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S') if tweet.created_at else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'text': tweet.text,
                    'user_name': 'user',
                    'user_location': '',
                    'retweet_count': metrics.get('retweet_count', 0),
                    'favorite_count': metrics.get('like_count', 0),
                    'hashtags': hashtags,
                    'search_query': search_query
                }
                tweets.append(tweet_data)
            
            return pd.DataFrame(tweets)
        else:
            print(f"No tweets found for query: {search_query}. Using mock data.")
            return generate_mock_tweets(search_query, count)
            
    except Exception as e:
        print(f"Error accessing Twitter API: {str(e)}. Using mock data instead.")
        return generate_mock_tweets(search_query, count)

def generate_mock_tweets(search_query, count=10):
    """Generate mock tweet data for development and testing"""
    mock_tweets = []
    
    positive_phrases = [
        "I love how", "Great progress on", "Exciting developments in", 
        "Impressive advances with", "Optimistic about"
    ]
    
    negative_phrases = [
        "Concerned about", "Disappointed with", "Worried that", 
        "Frustrated by", "Skeptical of"
    ]
    
    hashtag_options = {
        "climate change": ["ClimateAction", "GlobalWarming", "ClimateEmergency", "SaveEarth"],
        "renewable energy": ["CleanEnergy", "SolarPower", "WindEnergy", "Sustainability"],
        "sustainability": ["EcoFriendly", "GreenLiving", "ZeroWaste", "SustainableFuture"]
    }
    
    default_hashtags = ["Future", "Innovation", "Technology", "Progress"]
    
    for i in range(count):
        is_positive = random.random() > 0.5
        sentiment_phrases = positive_phrases if is_positive else negative_phrases
        
        phrase = random.choice(sentiment_phrases)
        tweet_text = f"{phrase} {search_query}. {'This could be a game changer!' if is_positive else 'We need better solutions.'}"
        
        relevant_hashtags = []
        for key in hashtag_options:
            if key.lower() in search_query.lower():
                relevant_hashtags.extend(hashtag_options[key])
        
        if not relevant_hashtags:
            relevant_hashtags = default_hashtags
            
        num_hashtags = random.randint(0, 3)
        selected_hashtags = random.sample(relevant_hashtags, min(num_hashtags, len(relevant_hashtags)))
        
        created_time = datetime.now() - timedelta(hours=random.randint(1, 72))
        mock_tweets.append({
            'id': f"mock_{i}_{int(datetime.now().timestamp())}",
            'created_at': created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'text': tweet_text,
            'user_name': f"user_{random.randint(1000, 9999)}",
            'user_location': random.choice(["New York", "London", "Tokyo", "Berlin", "Sydney", "", "Remote"]),
            'retweet_count': random.randint(0, 500),
            'favorite_count': random.randint(0, 1000),
            'hashtags': selected_hashtags,
            'search_query': search_query
        })
    
    print(f"Generated {count} mock tweets for: {search_query}")
    return pd.DataFrame(mock_tweets)

def save_tweets(df, output_path):
    """Save tweets to CSV file"""
    os.makedirs(output_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_path}/tweets_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} tweets to {filename}")
    return filename

if __name__ == "__main__":
    search_terms = ["climate change", "renewable energy", "sustainability"]
    
    all_tweets = pd.DataFrame()
    for term in search_terms:
        print(f"Extracting tweets for: {term}")
        tweets_df = extract_tweets(term, count=20)
        all_tweets = pd.concat([all_tweets, tweets_df])
    
    save_tweets(all_tweets, "data/raw")