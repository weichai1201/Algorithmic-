import csv
from datetime import datetime

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import Option
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.util.read_file import read_file

stock_filename = "src/data/sp500_adj_close_prices.csv"
stock_date_format = "%Y-%m-%d %H:%M:%S"  # 2004-01-02 00:00:00
stock_date_column_name = "Date"
tbills_filename = "src/data/T-Bills.csv"
tbills_date_format = "%d/%m/%Y"  # 16/01/2004
tbills_date_column_name = "DATE"


class DataAccessResult:
    def __init__(self, data: FinancialAsset | None, is_successful: bool = False):
        self.data = data
        self.is_successful = is_successful


def request_historical_price(symbol: Symbol, date: datetime, is_stock: bool = True) -> DataAccessResult:
    value = _retrieve_from_csv(symbol, date)
    if value < 0:
        return DataAccessResult(None)
    # is_stock might be redundant
    return DataAccessResult(Stock(symbol, Price(value, date)), True)


def retrieve_stock(symbol: Symbol, date: datetime) -> DataAccessResult:
    data = _retrieve_by_date(stock_filename, stock_date_column_name, date, stock_date_format)
    if symbol.symbol not in data.columns:
        return DataAccessResult(None)
    price = date[symbol.symbol]
    stock = Stock(symbol, Price(price, date))
    return DataAccessResult(stock, True)


def retrieve_rf(date: datetime):
    data = _retrieve_by_date(stock_filename, stock_date_column_name, date, stock_date_format)
    return DataAccessResult(data["DTB3"], True)


def _retrieve_from_csv(symbol: Symbol, date: datetime, filename: str = "src/data/sp500_adj_close_prices.csv"):
    column_date = "Date"
    date_format = "%Y-%m-%d %H:%M:%S"
    date_str = date.strftime(date_format)
    data = read_file(filename)
    if symbol.symbol not in data.columns:
        return -1
    return data[symbol.symbol][data[column_date] == date_str]


def _retrieve_by_date(filename: str, col_name: str, date: datetime, date_format=""):
    data = read_file(filename)
    date_str = date.strftime(date_format)
    return data[data[col_name] == date_str]
