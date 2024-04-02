from datetime import datetime
import numpy as np

from optionStrategy.stock_symbol import StockSymbol
from optionStrategy.stock import Stock
from optionStrategy.price import Price


class Option:
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price, expiration_date: datetime, premium: Price):
        self.stock_symbol = stock_symbol
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.premium = premium


class CallOption(Option):
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price, expiration_date: datetime, premium: Price):
        super().__init__(stock_symbol, strike_price, expiration_date, premium)
        self.option_type = "Call"

    def option_payoff(self, stock: Stock):
        return np.maximum(stock.current_price.price - self.strike_price.price, 0)


class PutOption(Option):
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price, expiration_date: datetime, premium: Price):
        super().__init__(stock_symbol, strike_price, expiration_date, premium)
        self.option_type = "Put"

    def option_payoff(self, stock: Stock):
        payoff = np.maximum(self.strike_price.price - stock.current_price.price, 0)
        return payoff
