{{ config(materialized='table') }}

SELECT
    id,
    created_utc,
    body,
    cleaned_text,
    vader_compound,
    vader_positive,
    vader_negative,
    vader_neutral,
    textblob_polarity,
    textblob_subjectivity,
    sentiment_category
FROM {{ source('raw_data', 'processed_reddit_comments') }} 