import urllib.request
import os
from heatmap_url_finder import get_url
from utils import get_date

def download_image():
    """
    Downloads the heatmap image from the URL provided by get_url()
    and saves it into the 'heatmaps' folder with today's date as the filename.
    """
    try:
        # Get the URL of the heatmap image
        url = get_url()

        # Get today's date for naming the file
        today = get_date()

        # Define the path where the image will be saved
        file_name = os.path.join("heatmaps", f"heatmap-{today}.png")

        # Download and save the image
        urllib.request.urlretrieve(url, file_name)
        print("Image downloaded successfully!")

    except Exception as e:
        print(f"Error downloading the image: {e}")

if __name__ == "__main__":
    try:
        download_image()
    except Exception as e:
        print(f"Unexpected error in 'download_image': {e}")
