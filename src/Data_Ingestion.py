import os
import requests
from auth import api_key
from auth import nyt_headline_api_key as story_api_key
from utils import break_date, get_date
from logger import logging

def get_articles():
    """
    Fetches articles and returns them as a single concatenated string with a separator.
    """
    try:
        formatted_date = get_date()
        article_date = break_date(formatted_date)
    except Exception as e:
        logging.error(f"Error getting or breaking the date: {e}")
        return ""

    key = api_key
    keywords = [
        "Stock Market", "Economy", "Earnings", "Bond Market", "Commodities",
        "Cryptocurrency", "IPOs", "Mergers and Acquisitions", "Regulation",
        "Stocks and Bonds", "Wall Street", "Stock Movers"
    ]
    separator = "\n---ARTICLE_SEPARATOR---\n"
    articles = []

    # Fetch articles from the NYT Search API
    try:
        for word in keywords:
            url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?&q={word}&facet_field=day_of_week&facet=true&begin_date={article_date}&sort=newest&api-key={key}"
            r = requests.get(url)

            try:
                for doc in r.json()["response"]["docs"]:
                    articles.append(doc['lead_paragraph'])
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
            if item["subsection"] == "economy" and item["abstract"] is not None:
                try:
                    articles.append(item["abstract"])
                except Exception as e:
                    logging.error(f"Error processing top story article: {e}")
    except Exception as e:
        logging.error(f"Error fetching top stories from the NYT Top Stories API: {e}")

    logging.info(f"Articles Ingested using Top Stories API")
    return separator.join(articles)

if __name__ == "__main__":
    try:
        get_articles()
    except Exception as e:
        logging.error(f"Unexpected error in 'get_articles': {e}")
