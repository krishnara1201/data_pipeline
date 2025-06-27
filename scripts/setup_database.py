# scripts/setup_database.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Set up PostgreSQL database for the project"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='twitter_sentiment'")
    if not cursor.fetchone():
        cursor.execute("CREATE DATABASE twitter_sentiment")
        print("Database created successfully")
    
    # Connect to the new database
    conn.close()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database="twitter_sentiment",
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_tweets (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP,
        text TEXT,
        user_name TEXT,
        user_location TEXT,
        retweet_count INTEGER,
        favorite_count INTEGER,
        hashtags TEXT,
        search_query TEXT,
        created_at_batch TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_tweets (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP,
        text TEXT,
        cleaned_text TEXT,
        user_name TEXT,
        user_location TEXT,
        retweet_count INTEGER,
        favorite_count INTEGER,
        search_query TEXT,
        vader_compound FLOAT,
        vader_positive FLOAT,
        vader_negative FLOAT,
        vader_neutral FLOAT,
        textblob_polarity FLOAT,
        textblob_subjectivity FLOAT,
        sentiment_category TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    print("Tables created successfully")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()