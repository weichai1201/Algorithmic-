from abc import abstractmethod
from datetime import datetime

from src.backtesting.agent import Agent
from src.trading_strategies.strategy.strategy_id import StrategyId


class Backtester:
    def __init__(self, start_date: datetime, end_date: datetime, self_agent:Agent, agents=list[Agent]):
        self._start_date = start_date
        self._end_date = end_date
        self._self_agent = self_agent
        self._agents = agents
        self._has_tested = False
        self._profits = dict[StrategyId, float]
        self._drawdowns = dict[StrategyId, float]
        self._cagr = 0.0

    @abstractmethod
    def run_back_testing(self):
        pass

    def get_profits(self):
        if not self._has_tested:
            self.run_back_testing()
        return self._profits

    def get_drawdowns(self):
        if not self._has_tested:
            self.run_back_testing()
        return self._drawdowns

    def get_profit(self, strategy_id: StrategyId):
        if not self._has_tested:
            self.run_back_testing()
        return self._profits[strategy_id]

    def get_drawdown(self, strategy_id: StrategyId):
        if not self._has_tested:
            self.run_back_testing()
        return self._drawdowns[strategy_id]

    def get_cagr(self):
        if not self._has_tested:
            self.run_back_testing()
        return self._cagr

    def summary(self):
        if not self._has_tested:
            self.run_back_testing()
        pass


class DailyMarketReplay (Backtester):
    def run_back_testing(self):
        pass


class MultiAgent (Backtester):
    pass

