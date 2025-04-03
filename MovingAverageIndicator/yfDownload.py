import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use("bmh")

def download_data(stock, start_date, end_date):
    # Download the data directly into a DataFrame
    ticker = yf.download(stock, start_date, end_date)
    
    # Create a DataFrame with just the Close price
    df = pd.DataFrame()
    df['Price'] = ticker['Close']
    
    # The date is already the index and in datetime format from yfinance
    # No need to set it manually
    
    return df

if __name__ == '__main__':
    start = '2010-01-05'
    end = '2015-01-05'
    stock_data = download_data('IBM', start, end)
    print(stock_data.head())  # Show the first few rows
    
    # Optional: Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data.index, stock_data['Price'])
    plt.title(f'IBM Stock Price ({start} to {end})')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.tight_layout()
    plt.savefig('IBM_Stocks.png')
    plt.show()