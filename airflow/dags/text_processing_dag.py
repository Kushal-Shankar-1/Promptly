from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for Airflow
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 21),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    "text_processing_pipeline",
    default_args=default_args,
    description="Extract and preprocess text from a PDF",
    schedule_interval="@daily",  # Runs daily
    catchup=False,
)

# Task 1: Extract text from PDF
extract_text = BashOperator(
    task_id="extract_text",
    bash_command="python /home/kushal/Promptly/data_ingestion/extract_text.py",
    dag=dag,
)

# Task 2: Preprocess extracted text
preprocess_text = BashOperator(
    task_id="preprocess_text",
    bash_command="python /home/kushal/Promptly/data_ingestion/preprocess_text.py",
    dag=dag,
)

# Define task dependencies
extract_text >> preprocess_text
