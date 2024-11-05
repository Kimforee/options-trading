import requests

# Alpha Vantage API key
api_key = "300DDTCL7F7V0CAB"
symbol = "MSFT"  # Microsoft's ticker symbol

# Alpha Vantage API endpoint for daily stock prices
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

# Make the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Check if the response contains the expected data structure
    if "Time Series (Daily)" in data:
        print("API Key is working! Here is a sample of the data:")
        # Print out the latest data point
        latest_date = list(data["Time Series (Daily)"].keys())[0]
        print(f"Date: {latest_date}")
        print(f"Data: {data['Time Series (Daily)'][latest_date]}")
    else:
        print("API Key is valid, but no data returned. Check API usage limits or parameters.")
else:
    print(f"Request failed with status code {response.status_code}. Check your API key and internet connection.")
