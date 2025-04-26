import os
import requests
from auth import api_key
from auth import nyt_headline_api_key as story_api_key
from utils import break_date, get_date
from logger import logging

def get_articles():
    """
    Fetches financial articles from the New York Times (NYT) using both
    the Article Search API and Top Stories API, and returns them as a single 
    concatenated string separated by a separator.
    """
    try:
        # Get today's formatted date and break it into the required format
        formatted_date = get_date()
        article_date = break_date(formatted_date)
    except Exception as e:
        logging.error(f"Error getting or breaking the date: {e}")
        return ""

    # Initialize API key for article search
    key = api_key

    # Define the list of keywords to search articles for
    keywords = [
        "Stock Market", "Economy", "Earnings", "Bond Market", "Commodities",
        "Cryptocurrency", "IPOs", "Mergers and Acquisitions", "Regulation",
        "Stocks and Bonds", "Wall Street", "Stock Movers"
    ]

    # Separator to distinguish between articles
    separator = "\n---ARTICLE_SEPARATOR---\n"
    articles = []

    # Fetch articles using the NYT Search API
    try:
        for word in keywords:
            url = (
                f"https://api.nytimes.com/svc/search/v2/articlesearch.json"
                f"?q={word}&facet_field=day_of_week&facet=true&begin_date={article_date}"
                f"&sort=newest&api-key={key}"
            )
            response = requests.get(url)

            try:
                # Extract 'lead_paragraph' from each document
                for doc in response.json()["response"]["docs"]:
                    articles.append(doc['lead_paragraph'])
            except Exception as e:
                logging.error(f"Error processing articles for keyword '{word}': {e}")
    except Exception as e:
        logging.error(f"Error fetching articles from the NYT Search API: {e}")

    logging.info("Articles ingested using Search API.")

    # Fetch top stories from the NYT Top Stories API (business section)
    try:
        url = f"https://api.nytimes.com/svc/topstories/v2/business.json?api-key={story_api_key}"
        response = requests.get(url).json()["results"]

        for item in response:
            # Filter top stories in the 'economy' subsection and ensure 'abstract' exists
            if item.get("subsection") == "economy" and item.get("abstract"):
                try:
                    articles.append(item["abstract"])
                except Exception as e:
                    logging.error(f"Error processing top story article: {e}")
    except Exception as e:
        logging.error(f"Error fetching top stories from the NYT Top Stories API: {e}")

    logging.info("Articles ingested using Top Stories API.")

    # Return the concatenated string of articles separated by the defined separator
    return separator.join(articles)

if __name__ == "__main__":
    try:
        get_articles()
    except Exception as e:
        logging.error(f"Unexpected error in 'get_articles': {e}")
