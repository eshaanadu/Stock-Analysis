import requests
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Set up the API request
def fetch_stock_data(symbol, api_key, start_date, end_date):
    base_url = "https://ftl.fasttrack.net/v1/"
    endpoint = f"historical_prices/{symbol}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    data = response.json()
    
    # Assuming the API returns a list of dictionaries with 'date' and 'close' keys
    data = pd.DataFrame(data)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    return data

# Step 2: Calculate moving averages
def calculate_moving_averages(data, windows=[20, 50]):
    for window in windows:
        data[f'SMA_{window}'] = data['close'].rolling(window=window).mean()
    return data

# Step 3: Visualize the data
def plot_data(data, symbol):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['close'], label='Closing Price')
    for column in data.columns:
        if 'SMA' in column:
            plt.plot(data.index, data[column], label=column)
    plt.title(f'{symbol} Stock Prices and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = input("Enter the stock symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    api_key = '2652353C-1BCF-4B23-AB40-1C9846C3F0A2'  # Replace with your FastTrack API key

    data = fetch_stock_data(symbol, api_key, start_date, end_date)
    data = calculate_moving_averages(data)
    plot_data(data, symbol)
