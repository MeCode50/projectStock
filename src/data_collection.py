import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import quandl

def collect_yahoo_data(ticker):
    data = yf.Ticker(ticker).history(period='1d', start='2010-01-01', end='2022-12-31')
    data.to_csv(f'{ticker}_yahoo.csv')
    return data

def collect_alpha_vantage_data(ticker, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, _ = ts.get_daily(symbol=ticker, outputsize='full')
    data.to_csv(f'{ticker}_alpha_vantage.csv')
    return data

def collect_quandl_data(ticker, api_key):
    quandl.ApiConfig.api_key = 'rSx6pne5RgB3uYsQnuqJ'
    data = quandl.get(f"WIKI/{ticker}")
    data.to_csv(f'{ticker}_quandl.csv')
    return data

# Example usage
yahoo_data = collect_yahoo_data('AAPL')
alpha_data = collect_alpha_vantage_data('AAPL', 'YOUR_ALPHA_VANTAGE_API_KEY')
quandl_data = collect_quandl_data('AAPL', 'YOUR_QUANDL_API_KEY')
