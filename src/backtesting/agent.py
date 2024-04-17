from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.transactions import Transactions


class Agent:
    # used in agent-based back testing. Assume to be no agents in simple daily market replay (single agent).
    # -strategies: Map < StrategyId, Strategy >
    # -transactions: Map < StrategyId, Transactions >

    def __init__(self, strategies: dict[StrategyId, Strategy]):
        self._strategies = strategies
        self.transactions = dict[StrategyId, Transactions]
        pass

