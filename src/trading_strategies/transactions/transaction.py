from datetime import datetime

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.transactions.positions import Positions


class Transaction:

    def __init__(self, positions: Positions, asset: FinancialAsset, time: datetime):
        self.__positions = positions
        self.__asset = asset
        self.__time = time

    def get_time(self):
        return self.__time

    def get_asset(self):
        return self.__asset

    def calculate_profit(self):
        pass

    def calculate_premium(self):
        return self.__asset.get_premium()

    def calculate_payoff(self, stock_price):
        return self.__asset.option_payoff(stock_price)