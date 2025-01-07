import urllib.request
from heatmap_url_finder import get_url
from utils import get_date
import os

def download_image():
    try:
        url = get_url()
        today = get_date()
        file_name = os.path.join("heatmaps", "heatmap-" + str(today) + ".png")
        urllib.request.urlretrieve(url, file_name)
        print("Image downloaded successfully!")
    except Exception as e:
        print("Error downloading the image:", str(e))

if __name__ == "__main__":
    download_image()