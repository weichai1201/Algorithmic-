from datetime import datetime

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.agent.transactions.position import Position
from src.agent.transactions.positions import Positions


class Transaction:

    def __init__(self, positions: Positions, asset: FinancialAsset, time: datetime, msg=""):
        self.__positions = positions
        self.__asset = asset
        self.__time = time
        self.__msg = msg
        self._realised_payoff = .0

    def get_time(self):
        return self.__time

    def get_asset(self):
        return self.__asset

    def calculate_premium(self):
        return self.__asset.get_premium()

    def calculate_payoff(self, stock_price):
        return self.__asset.option_payoff(stock_price)

    def is_short(self) -> bool:
        return self.__positions.position == Position.SHORT

    def is_long(self) -> bool:
        return self.__positions.position == Position.LONG

    def realise_payoff(self, amount: float):
        self._realised_payoff = amount

    def get_payoff(self):
        return self._realised_payoff

    def __str__(self):
        s = (f"Portfolio Entry:\n"
             f"  Positions: {self.__positions.__str__()}\n"
             f"  Asset: {self.__asset}\n"
             f"  Time: {self.__time}\n")
        if self.__msg != "":
            s += f"  Note: {self.__msg}\n"
        return s
