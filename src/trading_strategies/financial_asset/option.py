from abc import abstractmethod
from datetime import datetime
import numpy as np

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.price import Price


class Option(FinancialAsset):
    def __init__(self, symbol: Symbol, strike_price: Price, expiration_date: datetime, premium: Price):
        super().__init__()
        self._symbol = symbol
        self._strike_price = strike_price
        self._expiration_date = expiration_date
        self._premium = premium

    def price(self):
        return self._premium

    @property
    def symbol(self):
        return self._symbol

    @abstractmethod
    def in_the_money(self, stock_price: float) -> bool:
        pass

    @abstractmethod
    def itm_amount(self, stock_price: float) -> float:
        pass

    def get_strike(self):
        return self._strike_price

    def get_expiry(self):
        return self._expiration_date

    def get_premium(self):
        return self._premium

    def set_premium(self, premium):
        self._premium = premium

    def at_the_money(self, stock_price: float) -> bool:
        return self._strike_price.price() == stock_price

    def is_expired(self, time: datetime) -> bool:
        return time >= self._expiration_date

    def __str__(self):
        return (f"Option: {self._symbol}, "
                f"Strike Price: {self._strike_price},"
                f" Expiration Date: {self._expiration_date},"
                f" Premium: {self._premium}")

    @abstractmethod
    def option_payoff(self, stock: Stock):
        pass

    def payoff(self, optional) -> int:
        return self.option_payoff(optional)


class CallOption(Option):
    def __init__(self, symbol: Symbol, strike_price: Price, expiration_date: datetime, premium: Price):
        super().__init__(symbol, strike_price, expiration_date, premium)

    def in_the_money(self, stock_price: float) -> bool:
        return self.get_strike().price() < stock_price

    def itm_amount(self, stock_price: float) -> float:
        return max(0, stock_price - self.get_strike().price())

    def option_payoff(self, stock: Stock | float):
        if isinstance(stock, Stock):
            stock = stock.current_price.price()
        return np.maximum(stock - self.get_strike().price(), 0)


class PutOption(Option):
    def __init__(self, symbol: Symbol, strike_price: Price, expiration_date: datetime, premium: Price):
        super().__init__(symbol, strike_price, expiration_date, premium)

    def in_the_money(self, stock_price: float) -> bool:
        return self.get_strike().price() > stock_price

    def itm_amount(self, stock_price: float) -> float:
        return max(0, self.get_strike().price() - stock_price)

    def option_payoff(self, stock: Stock | float):
        if isinstance(stock, Stock):
            stock = stock.current_price.price()
        payoff = np.maximum(self.get_strike().price() - stock, 0)
        return payoff
