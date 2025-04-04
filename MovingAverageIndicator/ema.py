#!/usr/bin/env python3
"""
Exponential Moving Average (EMA) Analysis Script
Downloads stock data, calculates EMAs, plots results, and saves output
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import os

# Set matplotlib style
plt.style.use("bmh")

def download_data(stock, start, end):
    """
    Download stock price data from Yahoo Finance
    
    Args:
        stock (str): Stock ticker symbol
        start (datetime): Start date
        end (datetime): End date
    
    Returns:
        pd.DataFrame: DataFrame with Date index and Price column
    """
    try:
        print(f"Downloading {stock} data...")
        df = yf.download(stock, start, end)
        return df[['Close']].rename(columns={'Close': 'Price'})
    except Exception as e:
        print(f"Error downloading data: {e}")
        raise

def calculate_emas(data, short_period=50, long_period=200):
    """
    Calculate Exponential Moving Averages
    
    Args:
        data (pd.DataFrame): Price data
        short_period (int): Short EMA window (default: 50)
        long_period (int): Long EMA window (default: 200)
    
    Returns:
        pd.DataFrame: DataFrame with added EMA columns
    """
    try:
        data['Short EMA'] = data['Price'].ewm(span=short_period, adjust=False).mean()
        data['Long EMA'] = data['Price'].ewm(span=long_period, adjust=False).mean()
        return data.dropna()
    except Exception as e:
        print(f"Error calculating EMAs: {e}")
        raise

def plot_and_save(data, ticker):
    """
    Plot price and EMAs, save figure and data
    
    Args:
        data (pd.DataFrame): Data to plot
        ticker (str): Stock ticker for title/filename
    """
    try:
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(data['Price'], label='Stock Price', color='black', alpha=0.8)
        plt.plot(data['Short EMA'], label=f'Short EMA (50 days)', color='red', alpha=0.8)
        plt.plot(data['Long EMA'], label=f'Long EMA (200 days)', color='blue', alpha=0.8)
        
        # Format plot
        plt.title(f"{ticker} Price with Exponential Moving Averages")
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        
        # Create output directory if needed
        os.makedirs('output', exist_ok=True)
        
        # Save outputs
        plot_path = f"output/{ticker}_ema_plot.png"
        data_path = f"output/{ticker}_ema_data.csv"
        
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        data.to_csv(data_path)
        
        print(f"\nResults saved to:")
        print(f"- Plot: {plot_path}")
        print(f"- Data: {data_path}")
        
        plt.show()
        
    except Exception as e:
        print(f"Error generating plot: {e}")
        raise

if __name__ == '__main__':
    # Configuration
    TICKER = 'IBM'
    START_DATE = datetime.datetime(2010, 1, 1)
    END_DATE = datetime.datetime(2020, 1, 1)
    SHORT_EMA = 50    # days for short EMA
    LONG_EMA = 200    # days for long EMA
    
    try:
        # Download and process data
        stock_data = download_data(TICKER, START_DATE, END_DATE)
        stock_data = calculate_emas(stock_data, SHORT_EMA, LONG_EMA)
        
        # Show and save results
        print("\nLast 5 data points:")
        print(stock_data.tail())
        
        plot_and_save(stock_data, TICKER)
        
    except Exception as e:
        print(f"\nScript failed: {e}")