from abc import abstractmethod

from src.order.order import Order
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy_id import StrategyId


class Strategy:

    def __init__(self, id: StrategyId, symbol: Symbol):
        self._id = id
        self._symbol = symbol

    def id(self):
        return self._id

    def symbol(self) -> Symbol:
        return self._symbol

    def is_same_symbol(self, other: Symbol) -> bool:
        return self._symbol == other

