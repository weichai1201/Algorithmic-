from datetime import datetime
import numpy as np

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.price import Price


class Option(FinancialAsset):
    def __init__(self, symbol: Symbol, strike_price: Price, expiration_date: datetime, premium: Price):
        super().__init__()
        self.__symbol = symbol
        self.__strike_price = strike_price
        self.__expiration_date = expiration_date
        self.__premium = premium

    def get_symbol(self):
        return self.__symbol

    def get_strike(self):
        return self.__strike_price

    def get_expire(self):
        return self.__expiration_date

    def get_premium(self):
        return self.__premium

    def set_premium(self, premium):
        self.__premium = premium


class CallOption(Option):

    def option_payoff(self, stock: Stock):
        return np.maximum(stock.current_price.price - self.get_strike().price, 0)


class PutOption(Option):

    def option_payoff(self, stock: Stock):
        payoff = np.maximum(self.get_strike().price - stock.current_price.price, 0)
        return payoff
