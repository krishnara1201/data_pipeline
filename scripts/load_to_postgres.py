import os
import pandas as pd
from sqlalchemy import create_engine, text
import io

def load_processed_to_postgres(**kwargs):
    """Load processed Reddit comments CSV into PostgreSQL database"""
    # Get the processed file path from XCom
    ti = kwargs['ti']
    processed_file = ti.xcom_pull(task_ids='analyze_sentiment')
    
    # Database connection details
    db_user = os.getenv('POSTGRES_USER', 'airflow')
    db_pass = os.getenv('POSTGRES_PASSWORD', 'airflow')
    db_host = os.getenv('POSTGRES_HOST', 'postgres')
    db_name = os.getenv('POSTGRES_DB', 'airflow')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    table_name = 'processed_reddit_comments'
    schema = 'raw_data'

    # Create database connection
    connection_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_string)
    
    # Read the processed CSV file
    df = pd.read_csv(processed_file)
    print(f"Loaded CSV with {len(df)} rows and columns: {list(df.columns)}")
    
    # Clean and prepare the data
    # Convert created_utc to integer (it's currently float)
    if 'created_utc' in df.columns:
        df['created_utc'] = df['created_utc'].fillna(0).astype(int)
    
    # Fill NaN values in text columns
    text_columns = ['id', 'body', 'cleaned_text', 'sentiment_category']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna('')
    
    # Fill NaN values in numeric columns
    numeric_columns = ['vader_compound', 'vader_positive', 'vader_negative', 'vader_neutral', 
                      'textblob_polarity', 'textblob_subjectivity']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)
    
    # Select only the columns we want to insert
    columns_to_insert = ['id', 'created_utc', 'body', 'cleaned_text', 'vader_compound', 
                        'vader_positive', 'vader_negative', 'vader_neutral', 
                        'textblob_polarity', 'textblob_subjectivity', 'sentiment_category']
    
    # Filter DataFrame to only include columns that exist
    existing_columns = [col for col in columns_to_insert if col in df.columns]
    df_to_insert = df[existing_columns].copy()
    
    print(f"Prepared DataFrame with columns: {list(df_to_insert.columns)}")
    print(f"DataFrame shape: {df_to_insert.shape}")
    
    # Create table if it doesn't exist
    with engine.begin() as conn:
        # Drop table if exists
        conn.execute(text(f'DROP TABLE IF EXISTS {schema}.{table_name}'))
        
        # Create table with proper column types
        create_table_sql = f"""
        CREATE TABLE {schema}.{table_name} (
            id VARCHAR(255),
            created_utc BIGINT,
            body TEXT,
            cleaned_text TEXT,
            vader_compound FLOAT,
            vader_positive FLOAT,
            vader_negative FLOAT,
            vader_neutral FLOAT,
            textblob_polarity FLOAT,
            textblob_subjectivity FLOAT,
            sentiment_category VARCHAR(50)
        )
        """
        conn.execute(text(create_table_sql))
        
        # Use pandas to_sql to insert data
        df_to_insert.to_sql(
            name=table_name,
            schema=schema,
            con=engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000
        )
    
    print(f"Successfully loaded {len(df_to_insert)} rows from {processed_file} to {schema}.{table_name}")
    return f"{schema}.{table_name}" 