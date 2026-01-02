"""
Metrics module for calculating portfolio performance metrics.

This module provides functionality to compute daily returns, cumulative returns,
portfolio value over time, and other performance metrics.
"""

from typing import Tuple
import pandas as pd
import numpy as np


def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily returns for each ticker.
    
    Args:
        prices: DataFrame with historical prices (dates as index, tickers as columns)
        
    Returns:
        DataFrame with daily returns (percentage change)
        
    Example:
        >>> prices = download_price_data(['AAPL', 'MSFT'])
        >>> daily_returns = calculate_daily_returns(prices)
    """
    return prices.pct_change()


def calculate_cumulative_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative returns for each ticker.
    
    Args:
        prices: DataFrame with historical prices (dates as index, tickers as columns)
        
    Returns:
        DataFrame with cumulative returns
        
    Example:
        >>> prices = download_price_data(['AAPL', 'MSFT'])
        >>> cum_returns = calculate_cumulative_returns(prices)
    """
    return (prices / prices.iloc[0] - 1) * 100


def calculate_portfolio_value(positions: pd.DataFrame) -> pd.Series:
    """
    Calculate total portfolio value over time.
    
    Args:
        positions: DataFrame with position values (dates as index, tickers as columns)
        
    Returns:
        Series with total portfolio value over time
        
    Example:
        >>> portfolio_value = calculate_portfolio_value(positions)
    """
    return positions.sum(axis=1)


def calculate_portfolio_returns(
    portfolio_value: pd.Series, 
    initial_cost: float
) -> Tuple[pd.Series, float, float]:
    """
    Calculate portfolio returns over time.
    
    Args:
        portfolio_value: Series with portfolio value over time
        initial_cost: Initial cost basis of the portfolio
        
    Returns:
        Tuple of (daily_returns, total_return, percent_return)
        
    Example:
        >>> portfolio_value = calculate_portfolio_value(positions)
        >>> daily_ret, total_ret, pct_ret = calculate_portfolio_returns(portfolio_value, 10000)
    """
    # Daily returns
    daily_returns = portfolio_value.pct_change()
    
    # Total return
    current_value = portfolio_value.iloc[-1]
    total_return = current_value - initial_cost
    
    # Percent return
    percent_return = (total_return / initial_cost) * 100
    
    return daily_returns, total_return, percent_return


def calculate_portfolio_weights(positions: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate portfolio weights over time.
    
    Args:
        positions: DataFrame with position values (dates as index, tickers as columns)
        
    Returns:
        DataFrame with portfolio weights (percentages) over time
        
    Example:
        >>> weights = calculate_portfolio_weights(positions)
    """
    total_value = positions.sum(axis=1)
    weights = positions.div(total_value, axis=0) * 100
    return weights


def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
    """
    Calculate volatility (standard deviation of returns).
    
    Args:
        returns: Series of daily returns
        annualize: If True, annualize the volatility (default: True)
        
    Returns:
        Volatility value
        
    Example:
        >>> daily_returns = calculate_daily_returns(prices)
        >>> vol = calculate_volatility(daily_returns['AAPL'])
    """
    vol = returns.std()
    if annualize:
        vol = vol * np.sqrt(252)  # Assuming 252 trading days per year
    return vol


def calculate_sharpe_ratio(
    returns: pd.Series, 
    risk_free_rate: float = 0.02
) -> float:
    """
    Calculate Sharpe ratio (risk-adjusted return).
    
    Args:
        returns: Series of daily returns
        risk_free_rate: Annual risk-free rate (default: 2%)
        
    Returns:
        Sharpe ratio
        
    Example:
        >>> daily_returns = calculate_daily_returns(prices)
        >>> sharpe = calculate_sharpe_ratio(daily_returns['AAPL'])
    """
    # Annualized return
    annual_return = (1 + returns.mean()) ** 252 - 1
    
    # Annualized volatility
    annual_vol = calculate_volatility(returns, annualize=True)
    
    # Sharpe ratio
    if annual_vol == 0:
        return 0.0
    sharpe = (annual_return - risk_free_rate) / annual_vol
    
    return sharpe


def calculate_max_drawdown(portfolio_value: pd.Series) -> Tuple[float, str, str]:
    """
    Calculate maximum drawdown of portfolio.
    
    Args:
        portfolio_value: Series with portfolio value over time
        
    Returns:
        Tuple of (max_drawdown_pct, peak_date, trough_date)
        
    Example:
        >>> portfolio_value = calculate_portfolio_value(positions)
        >>> max_dd, peak, trough = calculate_max_drawdown(portfolio_value)
    """
    # Calculate running maximum
    running_max = portfolio_value.expanding().max()
    
    # Calculate drawdown
    drawdown = (portfolio_value - running_max) / running_max * 100
    
    # Find maximum drawdown
    max_drawdown = drawdown.min()
    
    # Find the dates
    trough_idx = drawdown.idxmin()
    peak_idx = portfolio_value.loc[:trough_idx].idxmax()
    
    return max_drawdown, str(peak_idx.date()), str(trough_idx.date())
