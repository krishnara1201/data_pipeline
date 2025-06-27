from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd

import sys
import os

sys.path.insert(0, os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')), 'scripts'))
from reddit_extraction import extract_reddit_comments, save_comments
from sentiment_analysis import process_tweets as process_sentiment
from load_to_postgres import load_processed_to_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['krish.narayanan1201@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'twitter_sentiment_analysis',
    default_args=default_args,
    description='A DAG for Twitter sentiment analysis',
    schedule=timedelta(days=5),
    start_date=datetime(2025, 5, 4),
    tags=['twitter', 'sentiment', 'nlp'],
)

# Define search terms
search_terms = ["climate change", "renewable energy", "sustainability"]

# Task to extract Reddit comments
def extract_and_save_reddit_comments(**kwargs):
    comments_df = extract_reddit_comments(subreddit_name='news', limit=100)
    output_path = "data/raw"
    os.makedirs(output_path, exist_ok=True)
    filename = save_comments(comments_df, output_path)
    kwargs['ti'].xcom_push(key='comments_file', value=filename)
    return filename

# Task to analyze sentiment
def analyze_comment_sentiment(**kwargs):
    ti = kwargs['ti']
    input_file = ti.xcom_pull(task_ids='extract_comments', key='comments_file')
    processed_df = process_sentiment(input_file)
    output_file = input_file.replace("raw", "processed")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    processed_df.to_csv(output_file, index=False)
    return output_file

# Define tasks
extract_task = PythonOperator(
    task_id='extract_comments',
    python_callable=extract_and_save_reddit_comments,
    dag=dag,
)

sentiment_task = PythonOperator(
    task_id='analyze_sentiment',
    python_callable=analyze_comment_sentiment,
    dag=dag,
)

# Run dbt models (assuming dbt is installed)
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /opt/airflow/sentiment_analysis && dbt run',
    dag=dag,
)

# Set task dependencies
extract_task >> sentiment_task >> dbt_run