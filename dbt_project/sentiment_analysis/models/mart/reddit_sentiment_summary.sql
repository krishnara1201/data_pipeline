{{ config(materialized='table') }}

SELECT
    sentiment_category,
    COUNT(*) as comment_count,
    AVG(vader_compound) as avg_vader_score,
    AVG(textblob_polarity) as avg_textblob_polarity,
    AVG(textblob_subjectivity) as avg_textblob_subjectivity
FROM {{ ref('stg_reddit_comments') }}
GROUP BY sentiment_category
ORDER BY sentiment_category