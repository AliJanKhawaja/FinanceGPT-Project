from openai import OpenAI
from auth import openai_api_key
from data_finder import get_data
from utils import get_date, letter_instructions, get_ticker_data
from logger import logging
import os

# Initialize OpenAI client
client = OpenAI()

def create_letter():
    """
    Creates a newsletter by generating content using OpenAI's API
    based on financial data and instructions, and saves it to a file.
    """
    # Get today's date to create a unique folder
    date = get_date()

    # Uncomment these lines to dynamically fetch data when ready
    # data = get_data()
    # data += get_ticker_data()

    # Ensure the directory for today's newsletter exists
    os.makedirs(f"news_letters/{date}", exist_ok=True)

    # Open (or create) the newsletter file
    with open(f"news_letters/{date}/news_letter_final.txt", "w") as file:
        # Uncomment below to enable OpenAI API call
        
        # messages = [
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": f"Turn the following data into a newsletter. Data: {data}. Use the following instructions: {letter_instructions}"}
        # ]
        
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=messages
        # )
        
        # article = completion.choices[0].message.content
        # file.write(article)
        # logging.info("Newsletter created successfully.")

        # Placeholder write for now
        file.write("Newsletter Created")
        print(date)
        logging.info("Newsletter created successfully.")

if __name__ == "__main__":
    try:
        create_letter()
    except Exception as e:
        logging.error(f"Unexpected error in 'create_letter': {e}")
