from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from src.heatmap_downloader import download_image
from src.logger import logging
import pendulum

# ---------------------- Timezone Setup ---------------------- #

# Define the local timezone (America/Chicago adjusts automatically for DST)
local_tz = pendulum.timezone("America/Chicago")

# ---------------------- DAG Definition ---------------------- #

with DAG(
    'heatmap_dag',
    description='DAG to download the market heatmap if the market is open',
    schedule_interval='59 17 * * 1-5',  # ⏰ 5:59 PM Houston Time (CST/CDT)
    start_date=datetime(2025, 1, 2, tzinfo=local_tz),
    catchup=False,
) as dag:

    @task
    def run_download_image():
        """
        Checks the market status from file and downloads the heatmap image
        only if the market was open.
        """
        try:
            with open("dags/src/market_status.txt", "r") as file:
                market_status = file.read().strip()

            if market_status == "open":
                download_image()
                logging.info("Heatmap download triggered successfully.")
            else:
                logging.info("Market is closed. Heatmap download skipped.")

        except Exception as e:
            logging.error(f"Error checking market status or downloading heatmap: {e}")

    # Define and run the task
    run_download_image_task = run_download_image()

    run_download_image_task
