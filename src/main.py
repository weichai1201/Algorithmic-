from datetime import datetime

from src.trading_strategies.financial_asset.option import PutOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing
from src.util.read_file import read_file
import pandas as pd


def main():
    file_path = '../src/data/sp500_adj_close_prices.csv'
    data = read_file(file_path)

    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[data['Date'] < '2014-01-01']
    aapl = filtered_data[['Date', 'AAPL']]

    aapl_symbol = Symbol('AAPL')
    historical_prices = [Price(price, timestamp) for price, timestamp in zip(aapl['AAPL'], aapl['Date'])]
    latest_price = Price(aapl.iloc[-1]['AAPL'], aapl.iloc[-1]['Date'])

    aapl_stock = Stock(aapl_symbol, latest_price, historical_prices)

    strike_price = Price(20.0, datetime(2014, 4, 18))
    premium = Price(0.0, datetime(2014, 4, 18))
    put_option = PutOption(aapl_symbol, strike_price, datetime(2014, 4, 18), premium)

    option_price = bsm_pricing(aapl_stock, put_option, 0.05)
    put_option.set_premium(option_price)

    pass

if __name__ == "__main__":
    main()