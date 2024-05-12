from abc import abstractmethod
from datetime import datetime, timedelta

import pandas as pd

from src.agent.agent import Agent
from src.backtesting.backtesting_summary import BacktestingSummary
from src.data_access.data_access import DataAccess
from src.trading_strategies.strategy.strategy_id import StrategyId


class Backtester:
    def __init__(self, start_date: datetime, end_date: datetime, self_agent: Agent, agents: list[Agent]):
        self._start_date = start_date
        self._end_date = end_date
        self._self_agent = self_agent
        self._agents = agents
        self._has_tested = False
        self._summary = None
        # register stock symbols for both agents
        self._symbols = self_agent.get_symbols()
        if (agents is not None) & len(agents) != 0:
            for agent in agents:
                self._symbols.add(agent.get_symbols())
        DataAccess().get_stock(self._symbols, start_date - timedelta(days=190), end_date)

    @abstractmethod
    def run_back_testing(self):
        pass

    def transactions(self, strategy_id: StrategyId):
        return self._self_agent.get_all_transactions()[strategy_id]

    # def get_profits(self):
    #     if not self._has_tested:
    #         self.run_back_testing()
    #     return self._profits
    #
    # def get_drawdowns(self):
    #     if not self._has_tested:
    #         self.run_back_testing()
    #     return self._drawdowns
    #
    # def get_profit(self, strategy_id: StrategyId):
    #     if not self._has_tested:
    #         self.run_back_testing()
    #     return self._profits[strategy_id]
    #
    # def get_drawdown(self, strategy_id: StrategyId):
    #     if not self._has_tested:
    #         self.run_back_testing()
    #     return self._drawdowns[strategy_id]
    #
    # def get_cagr(self):
    #     if not self._has_tested:
    #         self.run_back_testing()
    #     return self._cagr

    def summary(self, to_print=False):
        if not self._has_tested:
            self.run_back_testing()
        dates, payoffs, cumulative_payoffs, profits, cumulative_profits, drawdowns = self._self_agent.evaluate()
        self._summary = BacktestingSummary(0, 0,
                                           dates, profits, cumulative_profits, drawdowns,
                                           (self._end_date - self._start_date).days / 365)
        if to_print:
            return self._summary.__str__()
        return ""

    def get_data(self) -> dict[StrategyId, pd.DataFrame]:
        if self._summary is None:
            self.summary()
        return self._summary.get_data()


class MultiAgent(Backtester):
    pass
