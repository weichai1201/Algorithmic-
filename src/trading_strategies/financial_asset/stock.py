import os
import sys
import warnings
from datetime import datetime, timedelta

import numpy as np
import statistics
from arch import arch_model

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.util.read_file import get_historical_values

# file_path = '../src/data/sp500_adj_close_prices.csv'
file_path = 'data/sp500_adj_close_prices.csv'


class Stock(FinancialAsset):
    def __init__(self, symbol: Symbol, current_price: Price):
        super().__init__()
        self._symbol = symbol
        self.current_price = current_price
        # self.historical_price = historical_price
        # self.volatility = self.calculate_volatility()
        self._garch_long_run = -1

    def garch(self):
        if self._garch_long_run == -1:
            self._garch_long_run = self.calculate_garch()
        return self._garch_long_run

    def calculate_volatility(self):
        returns = self.get_returns()
        volatility = statistics.stdev(returns)
        return volatility

    def calculate_expected_return(self):
        returns = self.get_returns()
        return sum(returns) / len(returns)

    def get_returns(self):
        prices = [price for price in self.get_prices()]
        returns = np.diff(prices) / prices[:-1]
        return returns

    def get_prices(self):
        return get_historical_values(self.symbol, file_path, (self.current_price.time() - timedelta(days=182)).strftime('%Y-%m-%d'), self.current_price.time().strftime('%Y-%m-%d')).iloc[:, 1]

    def calculate_garch(self):
        returns = self.get_returns()
        model = arch_model(returns, vol='GARCH', p=1, q=1, rescale=False)
        fit = model.fit(disp='off')
        vol = np.sqrt(fit.forecast(horizon=100).variance).mean(axis=1).iloc[-1]
        return vol * np.sqrt(252)

    @property
    def symbol(self):
        return self._symbol

    def price(self) -> float:
        return self.current_price.price()

    def set_current_price(self, price):
        self.current_price = price

    def __str__(self):
        return f"Stock {self.symbol}: {self.current_price}"
