from abc import abstractmethod
from datetime import datetime

from src.data_access.data_package import DataPackage
from src.order.order import Order
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy_id import StrategyId


class Strategy:

    def __init__(self, id: StrategyId, symbol: Symbol):
        self._id = id
        self._symbol = symbol
        from src.agent.empty_agent import EmptyAgent
        self._agent = EmptyAgent()

    def id(self):
        return self._id

    def symbol(self) -> Symbol:
        return self._symbol

    def is_same_symbol(self, other: Symbol) -> bool:
        return self._symbol == other

    @abstractmethod
    def update(self, new_data: DataPackage) -> Order:
        pass

    @abstractmethod
    def need_update(self, date: datetime):
        return True

    def register_agent(self, agent):
        self._agent = agent

    def notify_agent(self, information):
        pass
