from datetime import timedelta, datetime

from src.agent.agent import Agent
from src.backtesting.backtester import Backtester
from src.data_access.data_access import retrieve_stock, retrieve_rf
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.option_pricing import bsm_pricing
from src.trading_strategies.strategy.option_strategy.option_strike import simulate_strikes


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

