from abc import abstractmethod
from datetime import datetime
from typing import Set

from src.backtesting.agent import Agent
from src.data_access.data_access import request_historical_price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.transaction import Transaction
from src.trading_strategies.transactions.transactions import Transactions


class Backtester:
    def __init__(self, start_date: datetime, end_date: datetime, self_agent: Agent, agents: list[Agent]):
        self._start_date = start_date
        self._end_date = end_date
        self._self_agent = self_agent
        self._transactions = list[Transaction]()
        self._agents = agents
        self._has_tested = False
        self._profits = dict[StrategyId, float]
        self._drawdowns = dict[StrategyId, float]
        self._cagr = 0.0

        # register stock symbols for both agents
        self._symbols = Set[Symbol]()
        self._symbols.add(self_agent.get_symbols())
        if (agents is not None) & len(agents) != 0:
            for agent in agents:
                self._symbols.add(agent.get_symbols())

    @abstractmethod
    def run_back_testing(self):
        pass

    def transactions(self):
        return self._transactions

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


class DailyMarketReplay(Backtester):
    def _update_by_symbol(self, agent: Agent, date: datetime):
        for symbol in self._self_agent.get_symbols():
            da_result = request_historical_price(symbol, date)
            if da_result.is_successful:
                transaction = self._self_agent.update(da_result.data)
                self._transactions.append(transaction)

    def run_back_testing(self):
        date = self._start_date
        while date < self._end_date:
            self._update_by_symbol(self._self_agent, date)
            for agent in self._agents:
                self._update_by_symbol(agent, date)
            date += 1


class MultiAgent(Backtester):
    pass
