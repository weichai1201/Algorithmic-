from abc import abstractmethod
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.agent.agent import Agent
from src.backtesting.backtesting_summary import BacktestingSummary
from src.data_access.data_access import retrieve_stock, retrieve_rf
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing
from src.trading_strategies.strategy.option_strategy.option_strike import simulate_strikes
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
        self._symbols = set[Symbol]()
        self._symbols.union(self_agent.get_symbols())
        if (agents is not None) & len(agents) != 0:
            for agent in agents:
                self._symbols.add(agent.get_symbols())

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
        dates, payoffs, profits, cumulative_profits, drawdowns = self._self_agent.evaluate()
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


class DailyMarketReplay(Backtester):
    def run_back_testing(self):
        self._has_tested = True
        date = self._start_date
        while date < self._end_date:
            self._update_by_symbol(self._self_agent, date)
            for agent in self._agents:
                self._update_by_symbol(agent, date)
            date += timedelta(days=1)

    def _update_by_symbol(self, agent: Agent, date: datetime):
        for symbol in agent.get_symbols():
            if not agent.need_update_for(date, symbol):
                continue
            da_result = retrieve_stock(symbol, date)
            if da_result.is_successful:
                stock: Stock
                stock = da_result.data
                # if np.isnan(stock.current_price):
                #     continue
                new_data = (stock.get_price().price(), self._simulate_premiums(stock, date))
                self._self_agent.update(symbol, new_data, date)

    @staticmethod
    def _simulate_premiums(stock: Stock, date: datetime, is_call=False):
        strikes = simulate_strikes(stock.get_price().price())
        result = dict[float, float]()
        for strike in strikes:
            expiry_date = date + timedelta(days=30)
            rf = retrieve_rf(expiry_date).data
            premium = bsm_pricing(stock, strike, expiry_date, [], rf, is_call)
            result[strike] = round(premium, 2)
        return result


class MultiAgent(Backtester):
    pass
