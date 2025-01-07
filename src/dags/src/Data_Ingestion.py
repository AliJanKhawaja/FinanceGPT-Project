import os
import requests
from auth import api_key
from auth import nyt_headline_api_key as story_api_key
from utils import break_date, get_date
from logger import logging

def get_articles():
    """
    This function takes in a date in the format of YYYYMMDD and returns a list of paths to the articles.
    """
    try:
        formatted_date = get_date()
        article_date = break_date(formatted_date)
    except Exception as e:
        logging.error(f"Error getting or breaking the date: {e}")
        return []

    try:
        # Create the directory for storing articles
        os.makedirs(f"data/{formatted_date}", exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating directory 'dags/src/data/{formatted_date}': {e}")
        return []

    key = api_key
    keywords = [
        "Stock Market", "Economy", "Earnings", "Bond Market", "Commodities",
        "Cryptocurrency", "IPOs", "Mergers and Acquisitions", "Regulation",
        "Stocks and Bonds", "Wall Street"
    ]
    count = 1
    paths = []

    # Fetch articles from the NYT Search API
    try:
        for word in keywords:
            url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?&q={word}&facet_field=day_of_week&facet=true&begin_date={article_date}&sort=newest&api-key={key}"
            r = requests.get(url)

            try:
                for doc in r.json()["response"]["docs"]:
                    with open(f"data/{formatted_date}/article_{count}.txt", "w") as file:
                        paths.append(f"data/{formatted_date}/article_{count}.txt")
                        file.write(doc['lead_paragraph'])
                    count += 1
            except Exception as e:
                logging.error(f"Error processing articles for keyword '{word}': {e}")
    except Exception as e:
        logging.error(f"Error fetching articles from the NYT Search API: {e}")

    logging.info(f"Articles Ingested using Search API")

    # Fetch top stories from the NYT Top Stories API
    try:
        url = f"https://api.nytimes.com/svc/topstories/v2/business.json?api-key={story_api_key}"
        r = requests.get(url).json()["results"]

        for item in r:
            if item["subsection"] == "economy":
                try:
                    with open(f"data/{formatted_date}/article_{count}.txt", "w") as file:
                        if item["abstract"] is not None:
                            file.write(item["abstract"])
                            paths.append(f"data/{formatted_date}/article_{count}.txt")
                    count += 1
                except Exception as e:
                    logging.error(f"Error writing top story article: {e}")
    except Exception as e:
        logging.error(f"Error fetching top stories from the NYT Top Stories API: {e}")

    logging.info(f"Articles Ingested using Top Stories API")
    return paths

if __name__ == "__main__":
    try:
        get_articles()
    except Exception as e:
        logging.error(f"Unexpected error in 'get_articles': {e}")
