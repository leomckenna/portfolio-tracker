# Portfolio Tracker

A Python-based portfolio tracker that uses yfinance to download stock prices, compute portfolio metrics, and visualize performance through a Streamlit dashboard.

## Features

- 📊 **Price Data Fetching**: Download adjusted close prices for multiple tickers using yfinance
- 💾 **Local Caching**: Cache raw price data locally for efficient reuse
- 📈 **Portfolio Metrics**: Calculate daily returns, total/percent return, portfolio weights, and portfolio value over time
- 📁 **Data Processing**: Save clean processed data tables
- 🎨 **Interactive Dashboard**: Streamlit dashboard showing portfolio value and allocation
- 🔧 **Modular Design**: Clean separation of concerns with fetch, holdings, and metrics modules
- 📝 **Type Hints & Docstrings**: Well-documented code with type hints

## Installation

1. Clone the repository:
```bash
git clone https://github.com/leomckenna/portfolio-tracker.git
cd portfolio-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Set Up Holdings

Create or edit `data/holdings.csv` with your portfolio holdings:

```csv
ticker,shares,avg_cost
AAPL,50,150.00
MSFT,30,250.00
GOOGL,20,100.00
TSLA,10,200.00
```

### 2. Process Portfolio Data

Run the processing script to download prices and compute metrics:

```bash
python process_portfolio.py
```

This will:
- Download historical price data for your holdings
- Cache the data locally in `data/raw/`
- Compute portfolio metrics
- Save processed data to `data/processed/`

### 3. Launch Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will show:
- Portfolio value over time
- Current allocation (pie chart)
- Holdings summary with returns
- Position values over time
- Key metrics (total value, return, max drawdown)

## Project Structure

```
portfolio-tracker/
├── data/
│   ├── holdings.csv          # Your portfolio holdings
│   ├── raw/                  # Cached price data (gitignored)
│   └── processed/            # Processed data outputs
├── src/
│   ├── fetch.py              # Price data fetching and caching
│   ├── holdings.py           # Holdings management
│   └── metrics.py            # Portfolio metrics calculation
├── dashboard.py              # Streamlit dashboard
├── process_portfolio.py      # Data processing script
└── requirements.txt          # Python dependencies
```

## Modules

### fetch.py
- `download_price_data()`: Download adjusted close prices with caching
- `get_latest_prices()`: Get most recent prices for tickers
- `clear_cache()`: Clear cached price data

### holdings.py
- `read_holdings()`: Read portfolio holdings from CSV
- `get_tickers()`: Extract ticker list from holdings
- `calculate_positions()`: Calculate position values over time
- `calculate_holdings_summary()`: Generate holdings summary with returns

### metrics.py
- `calculate_daily_returns()`: Compute daily returns
- `calculate_cumulative_returns()`: Compute cumulative returns
- `calculate_portfolio_value()`: Calculate total portfolio value
- `calculate_portfolio_returns()`: Calculate portfolio returns
- `calculate_portfolio_weights()`: Calculate portfolio weights over time
- `calculate_volatility()`: Calculate volatility
- `calculate_sharpe_ratio()`: Calculate Sharpe ratio
- `calculate_max_drawdown()`: Calculate maximum drawdown

## Output Files

The processing script generates the following files in `data/processed/`:

- `prices.csv`: Historical adjusted close prices
- `positions.csv`: Position values over time
- `portfolio_value.csv`: Total portfolio value over time
- `portfolio_weights.csv`: Portfolio weights over time
- `daily_returns.csv`: Daily returns for each ticker
- `cumulative_returns.csv`: Cumulative returns for each ticker
- `holdings_summary.csv`: Current holdings summary with returns

## Requirements

- Python 3.8+
- yfinance
- pandas
- numpy
- streamlit
