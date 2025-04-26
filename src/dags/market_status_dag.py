from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from market_status import get_market_status
import pendulum

# ---------------------- Timezone Setup ---------------------- #

# Define the local timezone (America/Chicago covers Houston and handles DST)
local_tz = pendulum.timezone("America/Chicago")

# ---------------------- DAG Definition ---------------------- #

with DAG(
    'market_status_dag',
    description='DAG to check and save US market status before newsletter generation',
    schedule_interval='59 17 * * 1-5',  # ⏰ 5:59 PM Houston Time (CST/CDT)
    start_date=datetime(2025, 1, 2, tzinfo=local_tz),
    catchup=False,
) as dag:

    @task
    def run_market_status():
        """
        Calls the get_market_status() function to fetch and store
        the current US market status (open/closed).
        """
        get_market_status()

    # Define and run the task
    run_market_status_task = run_market_status()

    run_market_status_task
