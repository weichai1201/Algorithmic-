import csv
from datetime import datetime

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import Option
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.util.read_file import read_file


class DataAccessResult:
    def __init__(self, data: FinancialAsset | None, is_successful: bool = False):
        self.data = data
        self.is_successful = is_successful


def request_historical_price(symbol: Symbol, date: datetime, is_stock: bool = True) -> DataAccessResult:
    value = retrieve_from_csv(symbol, date)
    if value < 0:
        return DataAccessResult(None)
    # is_stock might be redundant
    return DataAccessResult(Stock(symbol, Price(value, date)), True)


def retrieve_from_csv(symbol: Symbol, date: datetime, filename: str = "src/data/sp500_adj_close_prices.csv"):
    column_date = "Date"
    date_format = "%Y-%m-%d %H:%M:%S"
    date_str = date.strftime(date_format)
    data = read_file(filename)
    if symbol._symbol not in data.columns:
        return -1
    return data[symbol._symbol][data[column_date] == date_str]
