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

    def calculate_profit(self, other: "Transaction"):
        pass

    def __str__(self):
        return f"Portfolio Entry: Positions - {self.__positions}\n, Asset - {self.__asset}\n, Time - {self.__time}\n"