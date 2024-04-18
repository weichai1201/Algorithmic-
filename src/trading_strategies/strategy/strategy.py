from abc import abstractmethod

from src.order.order import Order
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy_id import StrategyId


class Strategy:

    def __init__(self, id: StrategyId, symbol: Symbol):
        self.id = id
        self.symbol = symbol

    @abstractmethod
    def symbol(self) -> Symbol:
        pass

    @abstractmethod
    def update(self) -> Order:
        pass

