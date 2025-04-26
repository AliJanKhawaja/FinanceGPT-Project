import os
from auth import openai_api_key, serp_api_key
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from Data_Ingestion import get_articles
from utils import get_date
from logger import logging

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPAPI_API_KEY"] = serp_api_key

def get_data():
    """
    Fetches articles' lead paragraphs using the NYT API, and processes each article
    to find more detailed, up-to-date information using a LangChain agent 
    with SerpAPI and Yahoo Finance tools.
    """
    # Initialize search tools
    search = SerpAPIWrapper(serpapi_api_key=serp_api_key)
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Use this tool to search the web for up-to-date information on a topic and give me a paragraph about it."
        ),
        YahooFinanceNewsTool()
    ]

    # Initialize ChatOpenAI LLM (zero temperature for deterministic results)
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        openai_api_key=openai_api_key
    )

    # Initialize agent with tools and LLM
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    # Fetch articles from NYT APIs
    articles_string = get_articles()
    if not articles_string:
        logging.error("No articles fetched.")
        return

    # Split the articles using the separator
    separator = "\n---ARTICLE_SEPARATOR---\n"
    articles = articles_string.split(separator)

    data = ""

    # Process each article individually
    for article in articles:
        try:
            result = agent.run(article)
        except Exception as e:
            logging.error(f"Error processing article: {e}")
            result = ""
        data += result + "\n\n"

    return data

if __name__ == "__main__":
    try:
        get_data()
    except Exception as e:
        logging.error(f"Unexpected error in 'get_data': {e}")
