import praw
import pandas as pd
import os

def extract_reddit_comments(subreddit_name='news', limit=100):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD')
    )
    comments = []
    for comment in reddit.subreddit(subreddit_name).comments(limit=limit):
        comments.append({
            'id': comment.id,
            'body': comment.body,
            'created_utc': comment.created_utc,
            'score': comment.score,
            'subreddit': subreddit_name
        })
    return pd.DataFrame(comments)

def save_comments(df, output_path):
    os.makedirs(output_path, exist_ok=True)
    filename = os.path.join(output_path, "reddit_comments.csv")
    df.to_csv(filename, index=False)
    return filename 