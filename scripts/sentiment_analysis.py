# scripts/sentiment_analysis.py
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import re

# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    """Clean and preprocess text data"""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user mentions
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Convert to lowercase
    text = text.lower().strip()
    return text

def analyze_sentiment(text):
    """Analyze sentiment using VADER and TextBlob"""
    # Handle NaN/None values
    if pd.isna(text) or text is None:
        text = ""
    
    # Ensure text is a string
    text = str(text)
    
    # VADER sentiment analysis
    sid = SentimentIntensityAnalyzer()
    vader_scores = sid.polarity_scores(text)
    
    # TextBlob sentiment analysis
    blob = TextBlob(text)
    textblob_polarity = blob.sentiment.polarity
    textblob_subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment category
    if vader_scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif vader_scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'vader_compound': vader_scores['compound'],
        'vader_positive': vader_scores['pos'],
        'vader_negative': vader_scores['neg'],
        'vader_neutral': vader_scores['neu'],
        'textblob_polarity': textblob_polarity,
        'textblob_subjectivity': textblob_subjectivity,
        'sentiment_category': sentiment
    }

def process_tweets(input_file):
    """Process tweets/Reddit comments and add sentiment analysis"""
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Determine the text column name (tweets use 'text', Reddit comments use 'body')
    if 'text' in df.columns:
        text_column = 'text'
    elif 'body' in df.columns:
        text_column = 'body'
    else:
        raise ValueError("No 'text' or 'body' column found in the CSV file")
    
    # Fill NaN values in text column
    df[text_column] = df[text_column].fillna("")
    
    # Clean the text
    df['cleaned_text'] = df[text_column].apply(clean_text)
    
    # Analyze sentiment with error handling
    sentiment_results = []
    for text in df['cleaned_text']:
        try:
            sentiment_result = analyze_sentiment(text)
            sentiment_results.append(sentiment_result)
        except Exception as e:
            print(f"Error analyzing sentiment for text: {text[:50]}... Error: {e}")
            # Use neutral sentiment as fallback
            sentiment_results.append({
                'vader_compound': 0.0,
                'vader_positive': 0.0,
                'vader_negative': 0.0,
                'vader_neutral': 1.0,
                'textblob_polarity': 0.0,
                'textblob_subjectivity': 0.0,
                'sentiment_category': 'neutral'
            })
    
    sentiment_df = pd.DataFrame(sentiment_results)
    
    # Combine with original data
    result_df = pd.concat([df, sentiment_df], axis=1)
    
    return result_df

if __name__ == "__main__":
    # Example usage
    input_file = "data/raw/tweets_20250503_123456.csv"  # Replace with your actual file
    processed_df = process_tweets(input_file)
    
    # Save the processed data
    output_file = input_file.replace("raw", "processed")
    processed_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")