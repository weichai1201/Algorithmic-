from src.optionStrategy.financial_asset.symbol import Symbol
from src.optionStrategy.strategy.strategy_id import StrategyId


class Strategy:

    def __init__(self, id: StrategyId, symbol: Symbol):
        self.id = id
        self.symbol = symbol

