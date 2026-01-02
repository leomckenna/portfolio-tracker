"""
Generate sample price data for testing when internet is not available.

This module creates synthetic historical price data for testing purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List


def generate_sample_prices(
    tickers: List[str],
    start_date: str = None,
    end_date: str = None,
    initial_prices: dict = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic price data for testing.
    
    Args:
        tickers: List of ticker symbols
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        initial_prices: Dict of initial prices for each ticker (optional)
        seed: Random seed for reproducibility (default: 42)
        
    Returns:
        DataFrame with historical prices
    """
    if end_date is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(end_date)
    
    if start_date is None:
        start_date = end_date - timedelta(days=365)
    else:
        start_date = pd.to_datetime(start_date)
    
    # Create date range (business days only)
    dates = pd.bdate_range(start=start_date, end=end_date)
    
    # Default initial prices if not provided
    if initial_prices is None:
        initial_prices = {
            'AAPL': 170.0,
            'MSFT': 350.0,
            'GOOGL': 140.0,
            'TSLA': 250.0,
            'AMZN': 145.0,
            'NVDA': 450.0,
        }
    
    # Generate price data
    data = {}
    np.random.seed(seed)  # For reproducibility
    
    for ticker in tickers:
        base_price = initial_prices.get(ticker, 100.0)
        
        # Generate returns with some trend and volatility
        daily_returns = np.random.normal(0.0005, 0.015, len(dates))
        
        # Add some trend
        trend = np.linspace(0, 0.2, len(dates))
        daily_returns += trend / len(dates)
        
        # Calculate prices
        prices = [base_price]
        for ret in daily_returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        data[ticker] = prices
    
    df = pd.DataFrame(data, index=dates)
    return df


if __name__ == "__main__":
    # Test the function
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    prices = generate_sample_prices(tickers)
    print("Generated sample prices:")
    print(prices.head())
    print(f"\nShape: {prices.shape}")
    print(f"Date range: {prices.index[0].date()} to {prices.index[-1].date()}")
