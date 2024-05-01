import os
import sys
import warnings

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
        prices = [p for p in prices if not np.isnan(p)]
        returns = np.diff(prices) / prices[:-1]
        return returns

    def get_prices(self, start_date='2004-01-01', end_date='2024-03-31'):
        return get_historical_values(self.symbol, file_path, start_date, end_date).iloc[:, 1]

    def calculate_garch(self, forecast_horizon=1000):
        with warnings.catch_warnings(action="ignore"):
            sys.stdout = open(os.devnull, 'w')
            returns = self.get_returns()
            model = arch_model(returns, vol='GARCH', p=1, q=1)
            fit = model.fit(show_warning=False)
            vol = np.sqrt(fit.forecast(horizon=forecast_horizon).variance).mean(axis=1).iloc[-1]
            sys.stdout = sys.__stdout__
            print("Run GARCH for {symbol} on the date {date}".
                  format(symbol=self.symbol, date=self.current_price.time().strftime("%Y-%m-%d")))
            return vol * np.sqrt(252)

    @property
    def symbol(self):
        return self._symbol

    def price(self) -> float:
        return self.current_price.price()

    def __str__(self):
        return f"Stock {self.symbol}: {self.current_price}"
