# Reddit Sentiment Analysis Pipeline

A data pipeline that extracts Reddit comments, performs sentiment analysis, and processes the data using Apache Airflow, dbt, and PostgreSQL.

## 🚀 Features

- **Reddit Data Extraction**: Fetches comments from r/news subreddit
- **Sentiment Analysis**: Uses VADER and TextBlob for sentiment scoring
- **Data Pipeline**: Apache Airflow orchestrates the entire workflow
- **Data Transformation**: dbt models for data cleaning and aggregation
- **Database Storage**: PostgreSQL for data persistence

## 📋 Prerequisites

- Docker and Docker Compose
- Reddit API credentials
- Git

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd data_pipeline_Project
```

### 2. Set Up Environment Variables

Copy the example environment file and fill in your credentials:
```bash
cp env.example .env
```

Edit `.env` file with your actual credentials:
```bash
# Reddit API Credentials
REDDIT_CLIENT_ID=your_actual_reddit_client_id
REDDIT_CLIENT_SECRET=your_actual_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent_string
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

### 3. Set Up Airflow Configuration

Copy the example Airflow configuration and generate secure keys:
```bash
cp airflow/config/airflow.cfg.example airflow/config/airflow.cfg
```

Generate secure keys for Airflow:
```bash
# Generate Fernet key for encryption
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate secret keys for API authentication
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

Edit `airflow/config/airflow.cfg` and replace the placeholder values:
- `YOUR_FERNET_KEY_HERE` with the generated Fernet key
- `YOUR_INTERNAL_API_SECRET_KEY_HERE` with a generated secret key
- `YOUR_SECRET_KEY_HERE` with a generated secret key
- `YOUR_JWT_SECRET_HERE` with a generated secret key

### 4. Start the Pipeline
```bash
docker-compose up -d
```

### 5. Access Airflow Web UI
- URL: http://localhost:8080
- Username: airflow
- Password: airflow

### 6. Trigger the DAG
- Go to the Airflow web UI
- Find the `twitter_sentiment_analysis` DAG
- Click "Trigger DAG" to run the pipeline

## 📁 Project Structure

```
data_pipeline_Project/
├── airflow/
│   ├── dags/                    # Airflow DAG definitions
│   └── config/                  # Airflow configuration
├── dbt_project/
│   └── sentiment_analysis/      # dbt models and configuration
├── scripts/                     # Python scripts for data processing
├── data/                        # Raw and processed data (gitignored)
├── docker-compose.yaml          # Docker services configuration
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (gitignored)
├── env.example                  # Example environment variables
└── README.md                    # This file
```

## 🔒 Security

### Protected Files
The following files are automatically ignored by Git to protect sensitive information:
- `.env` - Contains your actual API credentials
- `airflow/config/airflow.cfg` - Contains Airflow encryption keys and secrets
- `data/` - Contains raw and processed data
- `airflow/logs/` - Airflow log files
- `dbt_project/sentiment_analysis/profiles.yml` - Database connection details

### Environment Variables
All sensitive credentials are stored in environment variables:
- Reddit API credentials
- Database passwords
- Airflow secrets

## 📊 Data Flow

1. **Extract**: Reddit comments are fetched from r/news
2. **Transform**: Sentiment analysis is performed using VADER and TextBlob
3. **Load**: Data is saved to CSV files (database loading is optional)
4. **Model**: dbt models process and aggregate the data

## 🐛 Troubleshooting

### Common Issues

1. **Docker containers not starting**
   - Check if ports 8080 and 5432 are available
   - Ensure Docker has enough resources allocated

2. **Reddit API errors**
   - Verify your Reddit credentials in `.env`
   - Check Reddit API rate limits

3. **dbt model failures**
   - Check database connectivity
   - Verify dbt project configuration

### Logs
- Airflow logs: `airflow/logs/` (gitignored)
- Docker logs: `docker-compose logs <service-name>`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Important Notes

- Never commit your `.env` file to version control
- Keep your API credentials secure
- The pipeline processes public Reddit data only
- Respect Reddit's API terms of service and rate limits 