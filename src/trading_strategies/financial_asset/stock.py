import numpy as np
import statistics

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol


class Stock (FinancialAsset):
    def __init__(self, symbol: Symbol, current_price: Price, historical_price=list[Price]):
        super().__init__()
        self._symbol = symbol
        self.current_price = current_price
        self.historical_price = historical_price
        self.volatility = self.calculate_volatility()

    def calculate_volatility(self):
        returns = self.get_returns()
        volatility = statistics.stdev(returns)
        return volatility

    def calculate_expected_return(self):
        returns = self.get_returns()
        return sum(returns) / len(returns)

    def get_returns(self):
        prices = [price.get_price() for price in self.historical_price]
        returns = np.diff(prices) / prices[:-1]
        return returns

    @property
    def symbol(self):
        return self._symbol
