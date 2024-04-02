from datetime import datetime
import numpy as np

from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.price import Price


class Option:
    def __init__(self, symbol: Symbol, strike_price: Price, expiration_date: datetime, premium: Price):
        self.symbol = symbol
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.premium = premium


class CallOption(Option):

    def option_payoff(self, stock: Stock):
        return np.maximum(stock.current_price.price - self.strike_price.price, 0)


class PutOption(Option):

    def option_payoff(self, stock: Stock):
        payoff = np.maximum(self.strike_price.price - stock.current_price.price, 0)
        return payoff
