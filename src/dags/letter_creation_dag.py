from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from src.letter_creation import create_letter
from src.logger import logging
from airflow.utils.dates import days_ago
import pendulum

# ---------------------- Timezone Setup ---------------------- #

# Define the local timezone (America/Chicago covers Houston and adjusts automatically for DST)
local_tz = pendulum.timezone("America/Chicago")

# ---------------------- DAG Definition ---------------------- #

with DAG(
    'letter_creation_dag',
    description='DAG to create the newsletter if the market is open',
    schedule_interval='0 18 * * 1-5',  # 6:00 PM LOCAL TIME (CST/CDT)
    start_date=datetime(2025, 1, 2, tzinfo=local_tz),  # Start date with timezone awareness
    catchup=False,
) as dag:

    @task
    def run_letter_creation():
        """
        Checks the market status from file and triggers newsletter creation
        only if the market is open.
        """
        try:
            with open("dags/src/market_status.txt", "r") as file:
                market_status = file.read().strip()

            if market_status == "open":
                create_letter()
                logging.info("Newsletter creation triggered successfully.")
            else:
                logging.info("Market is closed. Newsletter creation skipped.")
        
        except Exception as e:
            logging.error(f"Error in reading market status or creating letter: {e}")

    # Define and run the task
    run_letter_creation_task = run_letter_creation()

    run_letter_creation_task
