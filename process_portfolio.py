"""
Main script to process portfolio data and generate reports.

This script orchestrates the portfolio analysis by:
1. Reading holdings from CSV
2. Downloading price data
3. Computing metrics
4. Saving processed data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetch import download_price_data, get_latest_prices
from holdings import read_holdings, get_tickers, calculate_positions, calculate_holdings_summary
from metrics import (
    calculate_daily_returns, 
    calculate_cumulative_returns,
    calculate_portfolio_value,
    calculate_portfolio_returns,
    calculate_portfolio_weights
)


def main():
    """Main function to process portfolio data."""
    print("=" * 60)
    print("Portfolio Tracker - Data Processing")
    print("=" * 60)
    
    # Read holdings
    print("\n1. Reading holdings from CSV...")
    holdings = read_holdings('data/holdings.csv')
    print(f"   Loaded {len(holdings)} holdings")
    print(holdings[['ticker', 'shares', 'avg_cost', 'cost_basis']].to_string(index=False))
    
    # Get tickers
    tickers = get_tickers(holdings)
    print(f"\n2. Tickers: {', '.join(tickers)}")
    
    # Download price data
    print("\n3. Downloading price data...")
    prices = download_price_data(tickers)
    print(f"   Downloaded data from {prices.index[0].date()} to {prices.index[-1].date()}")
    print(f"   Total trading days: {len(prices)}")
    
    # Get latest prices
    print("\n4. Getting latest prices...")
    latest_prices = get_latest_prices(tickers)
    for ticker, price in latest_prices.items():
        print(f"   {ticker}: ${price:.2f}")
    
    # Calculate positions
    print("\n5. Calculating positions...")
    positions = calculate_positions(holdings, prices)
    
    # Calculate portfolio value
    print("\n6. Calculating portfolio metrics...")
    portfolio_value = calculate_portfolio_value(positions)
    initial_cost = holdings['cost_basis'].sum()
    daily_returns, total_return, percent_return = calculate_portfolio_returns(
        portfolio_value, initial_cost
    )
    
    print(f"   Initial Cost: ${initial_cost:,.2f}")
    print(f"   Current Value: ${portfolio_value.iloc[-1]:,.2f}")
    print(f"   Total Return: ${total_return:,.2f}")
    print(f"   Percent Return: {percent_return:.2f}%")
    
    # Calculate portfolio weights
    weights = calculate_portfolio_weights(positions)
    print("\n   Current Portfolio Weights:")
    latest_weights = weights.iloc[-1].sort_values(ascending=False)
    for ticker, weight in latest_weights.items():
        print(f"   {ticker}: {weight:.2f}%")
    
    # Calculate daily returns for each ticker
    ticker_daily_returns = calculate_daily_returns(prices)
    
    # Calculate cumulative returns
    cumulative_returns = calculate_cumulative_returns(prices)
    
    # Create holdings summary
    holdings_summary = calculate_holdings_summary(holdings, latest_prices)
    
    # Save processed data
    print("\n7. Saving processed data...")
    os.makedirs('data/processed', exist_ok=True)
    
    # Save price data
    prices.to_csv('data/processed/prices.csv')
    print("   ✓ Saved prices.csv")
    
    # Save positions
    positions.to_csv('data/processed/positions.csv')
    print("   ✓ Saved positions.csv")
    
    # Save portfolio value
    portfolio_value.to_csv('data/processed/portfolio_value.csv', header=['value'])
    print("   ✓ Saved portfolio_value.csv")
    
    # Save portfolio weights
    weights.to_csv('data/processed/portfolio_weights.csv')
    print("   ✓ Saved portfolio_weights.csv")
    
    # Save daily returns
    ticker_daily_returns.to_csv('data/processed/daily_returns.csv')
    print("   ✓ Saved daily_returns.csv")
    
    # Save cumulative returns
    cumulative_returns.to_csv('data/processed/cumulative_returns.csv')
    print("   ✓ Saved cumulative_returns.csv")
    
    # Save holdings summary
    holdings_summary.to_csv('data/processed/holdings_summary.csv', index=False)
    print("   ✓ Saved holdings_summary.csv")
    
    print("\n" + "=" * 60)
    print("Processing complete! Data saved to data/processed/")
    print("=" * 60)


if __name__ == "__main__":
    main()
