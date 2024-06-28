import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='stock_analysis.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Function to fetch historical stock data from Twelve Data API
def fetch_stock_data(symbol, api_key, start_date, end_date):
    base_url = "https://api.twelvedata.com/time_series"
    params = {
        'symbol': symbol,
        'interval': '1day',  # Daily interval
        'start_date': start_date,  # Start date for historical data
        'end_date': end_date,  # End date for historical data
        'apikey': api_key,  # Your Twelve Data API key
        'format': 'json'  # Data format
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        if "values" not in data:
            logging.error(f"Error fetching data: {data.get('message', 'Unknown error')}")
            print("Error fetching data:", data.get("message", "Unknown error"))
            return None
        
        df = pd.DataFrame(data['values'])
        df['datetime'] = pd.to_datetime(df['datetime'])  # Convert datetime column to datetime objects
        df.set_index('datetime', inplace=True)  # Set datetime as the index
        df = df.apply(pd.to_numeric)  # Convert all columns to numeric
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        print(f"Request error: {e}")
        return None

# Function to calculate various technical indicators
def calculate_technical_indicators(data, include_ema=False, include_rsi=False, include_macd=False):
    data['SMA_20'] = data['close'].rolling(window=20).mean()  # Simple Moving Average (20 days)
    data['SMA_50'] = data['close'].rolling(window=50).mean()  # Simple Moving Average (50 days)
    
    if include_ema:
        data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean()  # Exponential Moving Average (20 days)
    if include_rsi:
        data['RSI'] = compute_rsi(data['close'], 14)  # Relative Strength Index (14 days)
    if include_macd:
        data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = compute_macd(data['close'])  # MACD
    
    return data

# Function to compute Relative Strength Index (RSI)
def compute_rsi(series, period):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Function to compute Moving Average Convergence Divergence (MACD)
def compute_macd(series, short_period=12, long_period=26, signal_period=9):
    short_ema = series.ewm(span=short_period, adjust=False).mean()
    long_ema = series.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    macd_signal = macd.ewm(span=signal_period, adjust=False).mean()
    macd_hist = macd - macd_signal
    return macd, macd_signal, macd_hist

# Function to visualize the stock prices and technical indicators
def plot_data(data, symbol, include_ema, include_rsi, include_macd):
    plt.figure(figsize=(14, 7))  # Set the figure size
    plt.plot(data.index, data['close'], label='Closing Price')  # Plot closing prices
    
    # Plot each moving average and technical indicator
    plt.plot(data.index, data['SMA_20'], label='SMA 20')
    plt.plot(data.index, data['SMA_50'], label='SMA 50')
    
    if include_ema and 'EMA_20' in data.columns:
        plt.plot(data.index, data['EMA_20'], label='EMA 20')
    if include_rsi and 'RSI' in data.columns:
        plt.plot(data.index, data['RSI'], label='RSI')
    if include_macd and 'MACD' in data.columns:
        plt.plot(data.index, data['MACD'], label='MACD')
        plt.plot(data.index, data['MACD_Signal'], label='MACD Signal')

    # Add titles and labels
    plt.title(f'{symbol} Stock Prices and Technical Indicators')
    plt.xlabel('Date')
    plt.ylabel('Price/Indicator Value')
    plt.legend()
    plt.show()  # Display the plot

# Function to summarize the lines displayed
def summarize_lines(include_ema, include_rsi, include_macd):
    summary = "The plot shows the closing prices, 20-day SMA, and 50-day SMA of the stock. "
    if include_ema:
        summary += "It also includes the 20-day EMA line. "
    if include_rsi:
        summary += "Additionally, it includes the RSI line. "
    if include_macd:
        summary += "Furthermore, it includes the MACD and MACD Signal lines. "
    print(summary)
    
    detailed_summary = """
    Summary of Technical Indicators:
    1. Closing Price: Represents the final price at which the stock traded on a particular day.
    2. SMA 20: The 20-day Simple Moving Average (SMA) is used to smooth out price data to identify the trend direction. When the SMA 20 is above the closing price, it indicates a bullish market.
    3. SMA 50: The 50-day SMA is similar to the 20-day SMA but calculated over a longer period, providing a smoother trend line.
    4. EMA 20: The 20-day Exponential Moving Average (EMA) gives more weight to recent prices and reacts more quickly to price changes. An EMA 20 above the closing price can indicate a bullish trend.
    5. RSI: The Relative Strength Index (RSI) measures the magnitude of recent price changes to evaluate overbought or oversold conditions. An RSI above 70 typically indicates an overbought condition, while an RSI below 30 indicates an oversold condition.
    6. MACD: The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages. The MACD line crossing above the MACD Signal line can indicate a bullish signal.
    """
    print(detailed_summary)

# Main function to execute the script
if __name__ == "__main__":
    # Get user inputs
    symbol = input("Enter the stock symbol: ")
    start_date = input("Enter the start date (MM/DD/YYYY): ")
    end_date = input("Enter the end date (MM/DD/YYYY): ")
    
    # Convert date format from 'MM/DD/YYYY' to 'YYYY-MM-DD'
    start_date = datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")

    api_key = '55ad01567d1d4b1f97c28e100a6ced31'  # Replace 'your_api_key_here' with your actual API key
    include_ema = input("Include EMA line? (yes/no): ").strip().lower() == 'yes'
    include_rsi = input("Include RSI line? (yes/no): ").strip().lower() == 'yes'
    include_macd = input("Include MACD line? (yes/no): ").strip().lower() == 'yes'

    # Fetch, process, and plot the data
    data = fetch_stock_data(symbol, api_key, start_date, end_date)
    if data is not None:
        data = calculate_technical_indicators(data, include_ema=include_ema, include_rsi=include_rsi, include_macd=include_macd)
        plot_data(data, symbol, include_ema, include_rsi, include_macd)
        summarize_lines(include_ema, include_rsi, include_macd)
