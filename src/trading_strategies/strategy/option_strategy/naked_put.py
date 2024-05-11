from datetime import datetime

from src.data_access.data_package import DataPackage
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.calculators.option_pricing import implied_date
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.calculators.option_strike import calculate_strike, roll_down_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.util.expiry_date import closest_expiration_date, nyse_calendar

risk_free_rate = 0.03


class NakedPut(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly,
                         weekday, num_of_strikes, scale)

    def roll_over(self, stock: Stock, expiration_date: datetime) -> (float, datetime):
        strike_price = calculate_strike(stock.get_price().price(), self._is_itm, self._num_of_strikes, True)
        # premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, True)
        # new_option = PutOption(stock.symbol(), Price(strike_price, stock.get_price().time()), expiration_date, premium)
        return strike_price, expiration_date

    def roll_down(self, stock, option, premium: float) -> (float, datetime):
        strike_price = roll_down_strike(stock.get_price().price(), option.get_strike().price(), self._num_of_strikes)
        new_expiration = implied_date(stock.get_price(), strike_price, risk_free_rate, premium,
                                      stock.calculate_garch(), True)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        # premium = bsm_pricing(stock, strike_price, new_expiration, [], risk_free_rate, True)
        # strike = Price(strike_price, stock.get_price().time())
        # new_option = PutOption(stock.symbol(), strike, new_expiration, premium)
        return strike_price, new_expiration

    def roll_up(self, stock, option, premium):
        pass

    def update(self, new_data: DataPackage):
        pass
