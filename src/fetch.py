"""
Fetch module for downloading and caching stock price data using yfinance.

This module provides functionality to download adjusted close prices for multiple
tickers and cache the raw data locally for efficient reuse.
"""

from typing import List, Dict
import os
import pickle
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd


def download_price_data(
    tickers: List[str], 
    start_date: str = None, 
    end_date: str = None,
    cache_dir: str = "data/raw"
) -> pd.DataFrame:
    """
    Download adjusted close prices for multiple tickers with local caching.
    
    Args:
        tickers: List of stock ticker symbols
        start_date: Start date in 'YYYY-MM-DD' format (default: 1 year ago)
        end_date: End date in 'YYYY-MM-DD' format (default: today)
        cache_dir: Directory to cache downloaded data
        
    Returns:
        DataFrame with dates as index and tickers as columns containing adjusted close prices
        
    Example:
        >>> tickers = ['AAPL', 'MSFT']
        >>> prices = download_price_data(tickers, start_date='2023-01-01', end_date='2023-12-31')
    """
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    
    # Create cache filename based on tickers and date range
    cache_file = os.path.join(
        cache_dir, 
        f"prices_{'_'.join(sorted(tickers))}_{start_date}_{end_date}.pkl"
    )
    
    # Try to load from cache
    if os.path.exists(cache_file):
        print(f"Loading cached data from {cache_file}")
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    print(f"Downloading price data for {len(tickers)} tickers from {start_date} to {end_date}...")
    
    # Download data from yfinance
    try:
        data = yf.download(
            tickers=tickers,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True  # Get adjusted close prices
        )
        
        # Handle single vs multiple tickers
        if len(tickers) == 1:
            # For single ticker, yfinance returns a DataFrame with columns like 'Close', 'Volume', etc.
            prices = data[['Close']].copy()
            prices.columns = tickers
        else:
            # For multiple tickers, get the 'Close' level
            prices = data['Close'].copy()
        
        # Check if we got any data
        if prices.empty or len(prices) == 0:
            raise ValueError("No data returned from yfinance")
        
    except Exception as e:
        print(f"Warning: Could not download real data from yfinance: {e}")
        print("Falling back to sample/synthetic data for demonstration...")
        
        # Import sample data generator
        from sample_data import generate_sample_prices
        prices = generate_sample_prices(tickers, start_date, end_date)
    
    # Cache the data
    with open(cache_file, 'wb') as f:
        pickle.dump(prices, f)
    print(f"Data cached to {cache_file}")
    
    return prices


def get_latest_prices(tickers: List[str]) -> Dict[str, float]:
    """
    Get the most recent closing prices for given tickers.
    
    Args:
        tickers: List of stock ticker symbols
        
    Returns:
        Dictionary mapping ticker symbols to their latest prices
        
    Example:
        >>> latest = get_latest_prices(['AAPL', 'MSFT'])
        >>> print(latest['AAPL'])
    """
    prices_df = download_price_data(tickers, start_date=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
    latest_prices = {}
    
    for ticker in tickers:
        if ticker in prices_df.columns:
            # Get the last valid price
            latest_prices[ticker] = prices_df[ticker].dropna().iloc[-1]
    
    return latest_prices


def clear_cache(cache_dir: str = "data/raw") -> None:
    """
    Clear all cached price data files.
    
    Args:
        cache_dir: Directory containing cached data
        
    Example:
        >>> clear_cache()
    """
    if os.path.exists(cache_dir):
        for file in os.listdir(cache_dir):
            if file.endswith('.pkl'):
                os.remove(os.path.join(cache_dir, file))
                print(f"Removed {file}")
