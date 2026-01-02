"""
Holdings module for managing portfolio holdings data.

This module provides functionality to read holdings from CSV files and 
compute portfolio positions and values.
"""

from typing import Dict, Tuple
import pandas as pd


def read_holdings(filepath: str = "data/holdings.csv") -> pd.DataFrame:
    """
    Read portfolio holdings from a CSV file.
    
    The CSV should have columns: ticker, shares, avg_cost
    
    Args:
        filepath: Path to the holdings CSV file
        
    Returns:
        DataFrame with holdings information
        
    Example:
        >>> holdings = read_holdings('data/holdings.csv')
        >>> print(holdings)
    """
    holdings = pd.read_csv(filepath)
    
    # Validate required columns
    required_columns = ['ticker', 'shares', 'avg_cost']
    for col in required_columns:
        if col not in holdings.columns:
            raise ValueError(f"Holdings CSV must contain '{col}' column")
    
    # Ensure correct data types
    holdings['shares'] = holdings['shares'].astype(float)
    holdings['avg_cost'] = holdings['avg_cost'].astype(float)
    
    # Calculate cost basis
    holdings['cost_basis'] = holdings['shares'] * holdings['avg_cost']
    
    return holdings


def get_tickers(holdings: pd.DataFrame) -> list:
    """
    Extract list of unique ticker symbols from holdings.
    
    Args:
        holdings: DataFrame containing holdings information
        
    Returns:
        List of ticker symbols
        
    Example:
        >>> holdings = read_holdings('data/holdings.csv')
        >>> tickers = get_tickers(holdings)
    """
    return holdings['ticker'].unique().tolist()


def calculate_positions(
    holdings: pd.DataFrame, 
    prices: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate current position values for all holdings.
    
    Args:
        holdings: DataFrame with holdings information (ticker, shares, avg_cost)
        prices: DataFrame with historical prices (dates as index, tickers as columns)
        
    Returns:
        DataFrame with position values over time
        
    Example:
        >>> holdings = read_holdings('data/holdings.csv')
        >>> prices = download_price_data(get_tickers(holdings))
        >>> positions = calculate_positions(holdings, prices)
    """
    positions = pd.DataFrame(index=prices.index)
    
    for _, row in holdings.iterrows():
        ticker = row['ticker']
        shares = row['shares']
        
        if ticker in prices.columns:
            positions[ticker] = prices[ticker] * shares
    
    return positions


def calculate_holdings_summary(
    holdings: pd.DataFrame, 
    latest_prices: Dict[str, float]
) -> pd.DataFrame:
    """
    Create a summary of holdings with current values and returns.
    
    Args:
        holdings: DataFrame with holdings information
        latest_prices: Dictionary mapping tickers to current prices
        
    Returns:
        DataFrame with holdings summary including current value and returns
        
    Example:
        >>> holdings = read_holdings('data/holdings.csv')
        >>> latest = get_latest_prices(get_tickers(holdings))
        >>> summary = calculate_holdings_summary(holdings, latest)
    """
    summary = holdings.copy()
    
    # Add current prices
    summary['current_price'] = summary['ticker'].map(latest_prices)
    
    # Calculate current value
    summary['current_value'] = summary['shares'] * summary['current_price']
    
    # Calculate returns
    summary['total_return'] = summary['current_value'] - summary['cost_basis']
    summary['percent_return'] = (summary['total_return'] / summary['cost_basis']) * 100
    
    # Calculate portfolio weight
    total_value = summary['current_value'].sum()
    summary['weight'] = (summary['current_value'] / total_value) * 100
    
    return summary
