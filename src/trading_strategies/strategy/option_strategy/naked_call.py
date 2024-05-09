from src.trading_strategies.financial_asset.option import Option, CallOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing, implied_date
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike, \
    roll_up_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.agent.transactions.position import Position
from src.util.expiry_date import closest_expiration_date, nyse_calendar

risk_free_rate = 0.03


class NakedCall(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, position: Position,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol, is_itm, position, is_weekly,
                         weekday, num_of_strikes, scale)

    def _roll_over(self, stock, expiration_date):
        strike_price = calculate_strike(stock.get_price().price(), self._is_itm, self._num_of_strikes, False)
        premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, False)
        new_option = CallOption(stock.symbol, Price(strike_price, stock.get_price().time()), expiration_date, premium)
        return new_option

    def _roll_up(self, stock, option, premium) -> Option:
        strike_price = roll_up_strike(stock.get_price().price(), option.get_strike().price(), self._num_of_strikes)
        new_expiration = implied_date(stock.get_price(), strike_price, risk_free_rate, premium,
                                      stock.calculate_garch(), False)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        premium = bsm_pricing(stock, strike_price, new_expiration, [], risk_free_rate, False)
        strike = Price(strike_price, stock.get_price().time())
        new_option = CallOption(stock.symbol, strike, new_expiration, premium)
        return new_option