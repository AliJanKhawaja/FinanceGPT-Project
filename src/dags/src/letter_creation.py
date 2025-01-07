import openai
from auth import openai_api_key
from data_finder import get_data
from utils import get_date
from heatmap_downloader import download_image
from utils import letter_instructions
from logger import logging

openai.api_key = openai_api_key

def create_letter():
    # download_image()
    # logging.info("Image downloaded")
    date = get_date()
    # get_data()
    # logging.info("Articles Ingested and Processed")

    with open(f"news_letters//{date}//news_letter.txt", "r") as file:
        data = file.read()



    with open(f"news_letters//{date}//news_letter_final.txt", "w") as file:
        article = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Turn the following data into a news letter. data: " + data + "\n" + f"use the following instructions {letter_instructions}"}])
        file.write(article.choices[0].message.content)
        logging.info("News Letter Created")


if __name__ == "__main__":
    create_letter()