"""
Streamlit Dashboard for Portfolio Tracker.

A simple dashboard showing portfolio value over time and current allocation.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetch import download_price_data, get_latest_prices
from holdings import read_holdings, get_tickers, calculate_positions, calculate_holdings_summary
from metrics import (
    calculate_portfolio_value,
    calculate_portfolio_returns,
    calculate_portfolio_weights,
    calculate_max_drawdown
)


# Page configuration
st.set_page_config(
    page_title="Portfolio Tracker",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Portfolio Tracker")
st.markdown("---")


@st.cache_data(ttl=300)  # Cache for 5 minutes (adjust based on market hours)
def load_portfolio_data():
    """Load and cache portfolio data."""
    holdings = read_holdings('data/holdings.csv')
    tickers = get_tickers(holdings)
    prices = download_price_data(tickers)
    latest_prices = get_latest_prices(tickers)
    positions = calculate_positions(holdings, prices)
    return holdings, prices, latest_prices, positions


# Load data
try:
    holdings, prices, latest_prices, positions = load_portfolio_data()
    
    # Calculate metrics
    portfolio_value = calculate_portfolio_value(positions)
    initial_cost = holdings['cost_basis'].sum()
    daily_returns, total_return, percent_return = calculate_portfolio_returns(
        portfolio_value, initial_cost
    )
    weights = calculate_portfolio_weights(positions)
    holdings_summary = calculate_holdings_summary(holdings, latest_prices)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Portfolio Value",
            f"${portfolio_value.iloc[-1]:,.2f}",
            f"{percent_return:.2f}%"
        )
    
    with col2:
        st.metric(
            "Total Return",
            f"${total_return:,.2f}",
            f"{percent_return:.2f}%"
        )
    
    with col3:
        st.metric(
            "Initial Cost",
            f"${initial_cost:,.2f}"
        )
    
    with col4:
        # Calculate max drawdown
        max_dd, peak_date, trough_date = calculate_max_drawdown(portfolio_value)
        st.metric(
            "Max Drawdown",
            f"{max_dd:.2f}%"
        )
    
    st.markdown("---")
    
    # Portfolio Value Over Time
    st.subheader("📊 Portfolio Value Over Time")
    
    portfolio_df = pd.DataFrame({
        'Portfolio Value': portfolio_value
    })
    st.line_chart(portfolio_df, height=400)
    
    st.markdown("---")
    
    # Two columns for allocation and holdings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥧 Current Allocation")
        
        # Get latest weights for pie chart
        latest_weights = weights.iloc[-1].to_dict()
        
        # Create pie chart data
        allocation_df = pd.DataFrame({
            'Ticker': list(latest_weights.keys()),
            'Weight': list(latest_weights.values())
        })
        
        # Display as bar chart (Streamlit doesn't have native pie chart)
        st.bar_chart(allocation_df.set_index('Ticker'))
        
        # Show percentages
        for ticker, weight in allocation_df.values:
            st.write(f"**{ticker}**: {weight:.2f}%")
    
    with col2:
        st.subheader("📋 Holdings Summary")
        
        # Format the summary for display
        display_summary = holdings_summary[[
            'ticker', 'shares', 'avg_cost', 'current_price', 
            'current_value', 'total_return', 'percent_return'
        ]].copy()
        
        # Format numeric columns
        display_summary['shares'] = display_summary['shares'].apply(lambda x: f"{x:.2f}")
        display_summary['avg_cost'] = display_summary['avg_cost'].apply(lambda x: f"${x:.2f}")
        display_summary['current_price'] = display_summary['current_price'].apply(lambda x: f"${x:.2f}")
        display_summary['current_value'] = display_summary['current_value'].apply(lambda x: f"${x:,.2f}")
        display_summary['total_return'] = display_summary['total_return'].apply(lambda x: f"${x:,.2f}")
        display_summary['percent_return'] = display_summary['percent_return'].apply(lambda x: f"{x:.2f}%")
        
        # Rename columns for display
        display_summary.columns = [
            'Ticker', 'Shares', 'Avg Cost', 'Current Price',
            'Current Value', 'Total Return', '% Return'
        ]
        
        st.dataframe(display_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Position Values Over Time
    st.subheader("📈 Position Values Over Time")
    st.line_chart(positions, height=400)
    
    st.markdown("---")
    
    # Additional Info
    with st.expander("ℹ️ About this Dashboard"):
        st.write("""
        This portfolio tracker dashboard provides:
        - **Real-time portfolio valuation** based on current market prices
        - **Performance metrics** including total return and percent return
        - **Portfolio allocation** showing the weight of each position
        - **Historical tracking** of portfolio value and individual positions
        - **Holdings summary** with detailed information for each position
        
        Data is fetched using yfinance and cached locally for efficiency.
        The dashboard automatically refreshes data every 5 minutes.
        """)
        
        st.write(f"**Last Updated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Data Range**: {prices.index[0].date()} to {prices.index[-1].date()}")

except FileNotFoundError:
    st.error("❌ Holdings file not found. Please create data/holdings.csv with columns: ticker, shares, avg_cost")
    st.info("""
    Example holdings.csv:
    ```
    ticker,shares,avg_cost
    AAPL,50,150.00
    MSFT,30,250.00
    GOOGL,20,100.00
    ```
    """)
except Exception as e:
    st.error(f"❌ Error loading portfolio data: {str(e)}")
    st.info("Please check your holdings file and ensure all required dependencies are installed.")
