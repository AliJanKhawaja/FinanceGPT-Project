from openai import OpenAI
from auth import openai_api_key
from data_finder import get_data
from utils import get_date, letter_instructions, get_ticker_data
from logger import logging
import os


client = OpenAI()

def create_letter():
    date = get_date()
    # data = get_data()
    # data += get_ticker_data()
    
    os.makedirs(f"news_letters/{date}", exist_ok=True)
    with open(f"news_letters/{date}/news_letter_final.txt", "w") as file:
    #     messages = [
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": f"Turn the following data into a newsletter. Data: {data}. Use the following instructions: {letter_instructions}"}
    #     ]
    #     completion = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=messages
    # )

    #     article = completion.choices[0].message.content
    #     file.write(article)
    #     logging.info("Newsletter Created")
        file.write("Newsletter Created")
        print(date)
        logging.info("Newsletter Created")
        

if __name__ == "__main__":
    create_letter()