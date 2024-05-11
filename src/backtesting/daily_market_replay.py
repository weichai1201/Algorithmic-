from datetime import timedelta, datetime

import numpy as np

from src.agent.agent import Agent
from src.backtesting.backtester import Backtester
from src.data_access.data_access import DataAccess
from src.data_access.data_package import DataPackage
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.option_pricing import bsm_pricing
from src.trading_strategies.strategy.option_strategy.option_strike import simulate_strikes


class DailyMarketReplay(Backtester):
    def __init__(self, start_date: datetime, end_date: datetime, self_agent: Agent, agents: list[Agent]):
        super().__init__(start_date, end_date, self_agent, agents)

    def run_back_testing(self):
        self._has_tested = True
        date = self._start_date
        while date <= self._end_date:
            if DataAccess().is_trading_in_historical(date):
                self._update_by_symbol(self._self_agent, date)
                for agent in self._agents:
                    self._update_by_symbol(agent, date)
            date += timedelta(days=1)

    @staticmethod
    def _update_by_symbol(agent: Agent, date: datetime):
        for symbol in agent.get_symbols():
            if not agent.need_update_for(date, symbol):
                continue
            stock_price = DataAccess().get_stock_price_at(symbol, date)
            if np.isnan(stock_price):
                continue
            data = DataPackage(date, Stock(symbol, Price(stock_price, date)))
            agent.update(symbol, data)
