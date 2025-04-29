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
