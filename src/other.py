from auth import openai_api_key
import os

# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = openai_api_key

# Import LangChain modules
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_openai import ChatOpenAI

# Initialize the ChatOpenAI LLM with zero temperature (deterministic output)
llm = ChatOpenAI(temperature=0.0)

# Initialize tools (Yahoo Finance News Tool)
tools = [YahooFinanceNewsTool()]

# Initialize the agent with LLM and tools
agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    try:
        # Example query about Apple stock news
        response = agent_chain.invoke(
            "What happened today with Apple stocks?"
        )
        print(response)
    except Exception as e:
        print(f"Error invoking agent: {e}")
