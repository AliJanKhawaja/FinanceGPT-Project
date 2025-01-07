import os
from auth import openai_api_key, serp_api_key
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from Data_Ingestion import get_articles
from utils import get_date
from logger import logging


os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPAPI_API_KEY"] = serp_api_key


def get_data():
    """
    Processes the articles' lead paragraphs returned returned by the NYT API and finds more information about it using the Langchain agent.
    """
    search = SerpAPIWrapper(serpapi_api_key=serp_api_key)
    tools = [
    Tool(
    name="Search",
    func=search.run,
    description="Use this tool to search the web for up-to-date information on the topic and give me a paragraph about it."
    ),
    YahooFinanceNewsTool()
    ]
    
    llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)
    
    agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
    )

    # data = agent.run("CES conference Las Vegas")
    # print(data)

    

    articles_string = get_articles()
    if not articles_string:
        logging.error("No articles fetched")
        return

    separator = "\n---ARTICLE_SEPARATOR---\n"
    articles = articles_string.split(separator)

    data = ""
    for article in articles:
        try:
            result = agent.run(article)
        except Exception as e:
            logging.error(f"Error processing article: {e}")
            result = ""
        data += result + "\n\n"       
    
    return data  


if __name__ == "__main__":
    get_data()










