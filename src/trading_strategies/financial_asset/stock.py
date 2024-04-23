import numpy as np
import statistics
from arch import arch_model

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.util.read_file import get_historical_values


# file_path = '../src/data/sp500_adj_close_prices.csv'
file_path = '/Users/yifanxiao/Desktop/csl.csv'

class Stock (FinancialAsset):
    def __init__(self, symbol: Symbol, current_price: Price):
        super().__init__()
        self._symbol = symbol
        self.current_price = current_price
        # self.historical_price = historical_price
        self.volatility = self.calculate_volatility()
        self.garch_long_run = self.get_garch()

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
        return get_historical_values(self.symbol, file_path, '2004-01-01', '2024-03-31').iloc[:, 1]

    def get_garch(self):
        returns = self.get_returns()
        model = arch_model(returns, vol='GARCH', p=1, q=1)
        fit = model.fit()
        vol = np.sqrt(fit.forecast(horizon=1000).variance).mean(axis=1)
        return vol * np.sqrt(252)


    @property
    def symbol(self):
        return self._symbol
