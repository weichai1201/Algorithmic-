from datetime import datetime
from typing import List, Tuple, Dict

from src.agent.agent import Agent
from src.trading_strategies.strategy.strategy_id import StrategyId


class MarginSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Margins:
    def __init__(self):
        self._margins: List[Tuple[datetime, float]] = list()

    def append_margin(self, date: datetime, margin: float):
        self._margins.append(tuple((date, margin)))

    def get_margins(self):
        return self._margins

class SimulatedMarket(metaclass=MarginSingletonMeta):
    def __init__(self):
        self._margins: Dict[Agent, Dict[StrategyId, Margins]] = dict()
