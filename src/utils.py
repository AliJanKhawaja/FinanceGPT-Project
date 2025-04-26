import datetime
import requests
from auth import vantage_api_key as api_key

# ----------------- Date Utilities ----------------- #

def break_date(formatted_date):
    """
    Breaks a formatted date (YYYY-MM-DD) into a compact string (YYYYMMDD).
    """
    month = formatted_date[5:7]
    day = formatted_date[8:10]
    year = formatted_date[0:4]
    return f"{year}{month}{day}"

def get_date():
    """
    Returns the current date formatted as YYYY-MM-DD,
    adjusted 6 hours back to better match financial market timings.
    """
    current_datetime = datetime.datetime.now() - datetime.timedelta(hours=6)
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    return formatted_date

# ----------------- Ticker Data Utilities ----------------- #

def get_ticker_data(tickers=["QQQ", "SPY"]):
    """
    Fetches intraday open, close, high, and low prices for given tickers (default: QQQ and SPY)
    and returns the results as a formatted string.
    """
    data_dict = {
        "QQQ Open": 0.00, "QQQ Close": 0.00, "QQQ Highest": 0.00, "QQQ Lowest": 0.00,
        "SPY Open": 0.00, "SPY Close": 0.00, "SPY Highest": 0.00, "SPY Lowest": 0.00
    }

    for ticker in tickers:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=60min&apikey={api_key}"
        r = requests.get(url)
        r_json = r.json()

        highest = 0.00
        lowest = 100000.00
        open_price = 0
        close_price = 0

        cur_date = get_date()

        try:
            for key, value in r_json["Time Series (60min)"].items():
                if key[:10] == cur_date:
                    if key[11:] == "04:00:00":
                        open_price = float(value["1. open"])
                        data_dict[f"{ticker} Open"] = open_price
                    if key[11:] == "19:00:00":
                        close_price = float(value["1. open"])
                        data_dict[f"{ticker} Close"] = close_price
                    if float(value["2. high"]) > highest:
                        highest = float(value["2. high"])
                    if float(value["3. low"]) < lowest:
                        lowest = float(value["3. low"])
        except Exception as e:
            print(f"Error processing ticker data for {ticker}: {e}")

        data_dict[f"{ticker} Highest"] = highest
        data_dict[f"{ticker} Lowest"] = lowest

    # Convert the dictionary to a string for printing
    data_str = "\n".join([f"{key}: {value}" for key, value in data_dict.items()])
    print(data_str)
    return data_str

def get_ticker_data_as_dict(tickers=["QQQ", "SPY"]):
    """
    Fetches intraday open, close, high, and low prices for given tickers
    and returns the results as a dictionary (instead of a formatted string).
    """
    data_dict = {
        "QQQ Open": 0.00, "QQQ Close": 0.00, "QQQ Highest": 0.00, "QQQ Lowest": 0.00,
        "SPY Open": 0.00, "SPY Close": 0.00, "SPY Highest": 0.00, "SPY Lowest": 0.00
    }

    for ticker in tickers:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=60min&apikey={api_key}"
        r = requests.get(url)
        r_json = r.json()

        highest = 0.00
        lowest = 100000.00
        open_price = 0
        close_price = 0

        cur_date = get_date()

        try:
            for key, value in r_json["Time Series (60min)"].items():
                if key[:10] == cur_date:
                    if key[11:] == "04:00:00":
                        open_price = float(value["1. open"])
                        data_dict[f"{ticker} Open"] = open_price
                    if key[11:] == "19:00:00":
                        close_price = float(value["1. open"])
                        data_dict[f"{ticker} Close"] = close_price
                    if float(value["2. high"]) > highest:
                        highest = float(value["2. high"])
                    if float(value["3. low"]) < lowest:
                        lowest = float(value["3. low"])
        except Exception as e:
            print(f"Error processing ticker data for {ticker}: {e}")

        data_dict[f"{ticker} Highest"] = highest
        data_dict[f"{ticker} Lowest"] = lowest

    return data_dict

# ----------------- Market Utilities ----------------- #

def get_market_status():
    """
    Fetches the current US market status (open/closed) from Alpha Vantage.
    """
    url = f"https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}"
    try:
        r = requests.get(url)
        data = r.json()
        us_status = data["markets"][0]["current_status"]
        return us_status
    except Exception as e:
        print(f"Error fetching market status: {e}")
        return "closed"

# ----------------- Newsletter Utilities ----------------- #

# Instructions provided to the AI for writing the newsletter
letter_instructions = (
    "
    You are an AI-generated financial newsletter named FinanceGPT. Make sure you start by
    mentioning that you are AI-generated and disclose that your data sources are New York Times,
    Yahoo Finance, and Alpha Vantage. There is no previous or new version of this newsletter, so do
    not mention that. Here are the stories: {stories} and here is the Stock Ticker Data: {ticker data}.
    Keep the context of the newsletter focused on the stories in the provided data. Keep in mind that
    this newsletter is for working professionals and students, so don’t make it too technical nor too
    simple. Use full forms to keep the vocabulary simple, for example, EPS should be earnings per
    share. Keep the word count between 450 and 650 words.
    "
)

def get_receivers(file_name):
    """
    Reads a file and returns a list of receiver emails, assuming one email per line.
    """
    try:
        with open(file_name, "r") as file:
            receivers = file.read().splitlines()
        return receivers
    except Exception as e:
        print(f"Error reading receivers list: {e}")
        return []

# ----------------- Main Execution ----------------- #

if __name__ == "__main__":
    get_ticker_data()
