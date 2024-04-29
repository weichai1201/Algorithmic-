import csv
from datetime import datetime, timedelta

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import Option
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.util.read_file import read_file

stock_filename = "data/sp500_adj_close_prices.csv"
stock_date_format = "%Y-%m-%d %H:%M:%S"  # 2004-01-02 00:00:00
stock_date_column_name = "Date"
tbills_filename = "data/T-Bills.csv"
tbills_date_format = "%d/%m/%Y"  # 16/01/2004
tbills_date_column_name = "DATE"


class DataAccessResult:
    def __init__(self, data: float | Stock | FinancialAsset | None, is_successful: bool = False):
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
    if len(data) == 0 or symbol.symbol not in data.columns:
        return DataAccessResult(None)
    price = data[symbol.symbol].values[0]
    stock = Stock(symbol, Price(price, date))
    return DataAccessResult(stock, True)


def retrieve_rf(date: datetime):
    result = _retrieve_by_date(tbills_filename, tbills_date_column_name, date, tbills_date_format)
    traceback_days = 10
    i = 0
    # in case risk free is not available on that date, search back a few days before.
    while len(result) == 0 and i < traceback_days:
        date = date - timedelta(days=1)
        result = _retrieve_by_date(tbills_filename, tbills_date_column_name, date, tbills_date_format)
        i += 1
    if len(result) == 0:
        return DataAccessResult(None)
    result = result["DTB3"].values[0]
    if result == ".":
        return retrieve_rf(date - timedelta(days=1))
    return DataAccessResult(float(result) / 100, True)


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
    result = data[data[col_name] == date_str]
    return data[data[col_name] == date_str]
