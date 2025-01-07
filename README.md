# FinanceGPT

_A fully automated AI generated Newsletter covering Macroeconomics and Stock Market News._
![](https://wp.stocktwits.com/wp-content/uploads/sites/2/2025/01/06172555/Finviz-Heatmap-01-06-25.png?_bhlid=08c737ec236972b0fd257580d7e3896d6fa0a99c)

## Introduction

The FinanceGPT project leverages the capabilities of AI and various APIs to create a daily newsletter that covers Macroeconomics and Stock Market-related topics. The project uses AI language generation to craft newsletter content, pulls relevant news from the New York Times "Top Stories" API, gathers stock ticker data from AlphaVantage API, and extracts insights from Langchain-connected GPT-4 model.

## Features

- AI-Generated Content: The newsletter content is fully autonomous, generated using OPENAI's GPT-4 model, ensuring engaging and relevant updates.
- Data Aggregation: The project aggregates macroeconomic news from the New York Times API and stock data from the AlphaVantage API.
- In-depth Insights: Langchain framework is employed to extract deeper insights from the top stories retrieved from the New York Times API. It uses Google Seach Agent and Yahoo Finance Agent.
- Automation: Apache Airflow is used to schedule the entire process, ensuring the newsletter is generated a specific time of the day.

## Technologies Used

- OPENAI GPT-4o-mini: AI language model for generating newsletter content.
- New York Times API: Source of macroeconomic and stock-related news.
- AlphaVantage API: Provides stock ticker data for QQQ and SPY.
- Langchain: Framework connecting GPT-4 with the internet to extract insights.
- Python: Main programming language for scripting and data processing.
- Apache Airflow: Automation tool for scheduling and managing the daily newsletter generation.

## Setup Instructions

_To set up the GPT NewsLetter project locally, follow these steps:_

1. Clone the repository
2. Set up the required APIs: Obtain API keys for New York Times, AlphaVantage and Google Serp.
3. pip install all the libraries in requirement.txt file
4. run the script letter_creation.py
5. Set up Apache Airflow and configure the scheduled task for the newsletter generation.(optional)

## Usage

- Ensure all APIs and frameworks are set up and configured properly.
- Run the Python scripts to pull news from the New York Times API and stock data from AlphaVantage API.
- Use Langchain to gather insights from the retrieved news.
- Generate the newsletter content using GPT-4.
- Automate the newsletter through the scheduled Apache Airflow task(optional)

## Automation

The FinanceGPT project is designed to be fully automated using Apache Airflow. The scheduled workflow involves running the necessary Python scripts and generating the newsletter content at a specific time every day. This automation ensures consistent and timely delivery of the newsletter to subscribers.

## Contributing

Contributions to this project are welcome! If you have ideas for improvements or new features, please follow these steps:

- Fork the repository.
- Create a new branch for your feature: git checkout -b feature-name
- Commit your changes: git commit -m "Add new feature"
- Push to the branch: git push origin feature-name
- Open a pull request, describing your feature and the changes you've made.
- Contact Information

For questions, suggestions, or feedback, please contact the project maintainer at alijaan1234@gmail.com. I appreciate your interest and contributions!
Thank you for using FinanceGPT for staying updated on Macroeconomics and Stock Market news!
