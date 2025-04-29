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
