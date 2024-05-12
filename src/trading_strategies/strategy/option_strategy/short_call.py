from datetime import datetime
from typing import List

from src.data_access.data_package import DataPackage
from src.market.order import Order
from src.trading_strategies.financial_asset.option import Option, CallOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.calculators.option_pricing import implied_date
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.calculators.option_strike import calculate_strike, \
    roll_up_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.agent.transactions.position import Position
from src.util.expiry_date import closest_expiration_date, nyse_calendar

risk_free_rate = 0.03


class ShortCall(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly,
                         weekday, num_of_strikes, scale)

    def roll_over(self, stock, expiration_date) -> (float, datetime):
        strike_price = calculate_strike(stock.get_price().price(), self._is_itm, self._num_of_strikes, False)
        return strike_price, expiration_date

    def roll_up(self, stock, option, premium) -> (float, datetime):
        strike_price = roll_up_strike(stock.get_price().price(), option.get_strike().price(), self._num_of_strikes)
        new_expiration = implied_date(stock.get_price(), strike_price, risk_free_rate, premium,
                                      stock.calculate_garch(), False)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        return strike_price, new_expiration

    def update(self, new_data: DataPackage) -> List[Order]:
        pass
