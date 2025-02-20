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
    schedule_interval="@once",  # ✅ Run immediately for testing
    catchup=False,
)

# ✅ Ensure Airflow starts in the correct working directory
extract_text = BashOperator(
    task_id="extract_text",
    bash_command="cd /home/kushal/Promptly && python src/data_ingestion/extract_text.py",
    dag=dag,
)

preprocess_text = BashOperator(
    task_id="preprocess_text",
    bash_command="cd /home/kushal/Promptly && python src/data_ingestion/preprocess_text.py",
    dag=dag,
)

# Define task dependencies
extract_text >> preprocess_text
