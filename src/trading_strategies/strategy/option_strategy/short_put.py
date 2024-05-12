from datetime import datetime
from typing import List

from src.data_access.data_access import DataAccess
from src.data_access.data_package import DataPackage
from src.data_access.volatility import VolatilityType, Volatility
from src.market.order import Order
from src.trading_strategies.financial_asset.option import Option
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.calculators.option_pricing import implied_date
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.calculators.option_strike import calculate_strike, \
    roll_down_strike, get_strike_gap
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.util.calculate_volatility import calculate_vol
from src.util.expiry_date import closest_expiration_date, nyse_calendar, next_expiry_date


class ShortPut(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly,
                         weekday, num_of_strikes, scale)

    def roll_over(self, stock: Stock, date: datetime) -> (float, datetime):
        strike_price = calculate_strike(stock.get_price().price(), self._is_itm, self._num_of_strikes, True)
        expiration_date = next_expiry_date(date, is_weekly=self._is_weekly, weekday=self._weekday)
        return strike_price, expiration_date

    def roll_down(self, stock_price: float, date: datetime, prev_option: Option) -> (float, datetime):
        prev_strike = prev_option.get_strike().price()
        symbol = prev_option.symbol()
        # strike
        strike_price = roll_down_strike(stock_price, prev_strike, self._num_of_strikes)
        # expiration
        sigma = DataAccess().get_volaitlity(symbol, VolatilityType.GARCH, date).value
        risk_free_rate = DataAccess().get_risk_free(date).value
        premium = prev_option.itm_amount(stock_price) + get_strike_gap(stock_price)
        new_expiration = implied_date(stock_price, date, strike_price, risk_free_rate, premium, sigma, True)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        return strike_price, new_expiration

    def roll_up(self,  stock_price: float, option: Option, premium: float) -> (float, datetime):
        pass

    def update(self, new_data: DataPackage) -> List[Order]:
        pass
