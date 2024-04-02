from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy_id import StrategyId


class Strategy:

    def __init__(self, id: StrategyId, symbol: Symbol):
        self.id = id
        self.symbol = symbol

