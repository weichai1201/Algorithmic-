from datetime import datetime

from src.trading_strategies.transactions.positions import Positions


class Transaction:

    def __init__(self, positions: Positions, time: datetime):
        self.__positions = positions
        self.__time = time

    def get_time(self):
        return self.__time

    def calculate_profit(self, other: "Transaction"):
        pass
