#!/usr/bin/env python3
"""
Simple Moving Average (SMA) Analysis
- Downloads stock data
- Calculates SMAs only (no other indicators)
- Saves plot as PNG
- Saves data as CSV
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import os

# Configuration - Edit these values as needed
TICKER = "IBM"
START_DATE = datetime.datetime(2010, 1, 1)
END_DATE = datetime.datetime(2020, 1, 1)
SHORT_SMA_DAYS = 50   # Short-term SMA window
LONG_SMA_DAYS = 200   # Long-term SMA window
OUTPUT_DIR = "output" # Directory for saved files

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_stock_data(ticker, start, end):
    """
    Download stock price data
    Returns: DataFrame with 'Price' column and datetime index
    """
    print(f"Downloading {ticker} data...")
    df = yf.download(ticker, start, end)
    return df[['Close']].rename(columns={'Close': 'Price'})

def calculate_sma(data, window):
    """Calculate Simple Moving Average"""
    return data['Price'].rolling(window=window).mean()

def generate_plot(data, ticker):
    """Create and save SMA plot"""
    plt.figure(figsize=(12, 6))
    
    # Plot data
    plt.plot(data['Price'], label='Price', color='black', linewidth=1)
    plt.plot(data['SMA_50'], label='50-day SMA', color='blue', linewidth=1.5)
    plt.plot(data['SMA_200'], label='200-day SMA', color='red', linewidth=1.5)
    
    # Formatting
    plt.title(f"{ticker} Price with Simple Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    
    # Save and show
    plot_path = f"{OUTPUT_DIR}/{ticker}_sma_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {plot_path}")
    plt.show()

def save_data(data, ticker):
    """Save data to CSV"""
    csv_path = f"{OUTPUT_DIR}/{ticker}_sma_data.csv"
    data.to_csv(csv_path)
    print(f"Data saved to {csv_path}")

if __name__ == "__main__":
    ensure_output_dir()
    
    # Get data
    stock_data = download_stock_data(TICKER, START_DATE, END_DATE)
    
    # Calculate SMAs
    stock_data['SMA_50'] = calculate_sma(stock_data, SHORT_SMA_DAYS)
    stock_data['SMA_200'] = calculate_sma(stock_data, LONG_SMA_DAYS)
    stock_data.dropna(inplace=True)  # Remove incomplete SMA rows
    
    # Output results
    save_data(stock_data, TICKER)
    generate_plot(stock_data, TICKER)
    
    # Show final data sample
    print("\nLast 5 data points:")
    print(stock_data.tail())