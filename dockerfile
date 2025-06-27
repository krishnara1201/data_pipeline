FROM apache/airflow:3.0.0-python3.10

COPY requirements.txt /requirements.txt

# Remove Windows-specific packages
#RUN sh -c "grep -v 'pywin32' /requirements.txt > /requirements-filtered.txt"

USER airflow
RUN pip install -r /requirements.txt