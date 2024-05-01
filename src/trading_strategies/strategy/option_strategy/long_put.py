from src.trading_strategies.financial_asset.option import PutOption, Option
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing, implied_date
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike, roll_down_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.util.expiry_date import closest_expiration_date, nyse_calendar

risk_free_rate = 0.03


class LongPut(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, position: Position,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol, is_itm, position, is_weekly,
                         weekday, num_of_strikes, scale)

    def _roll_over(self, stock, expiration_date):
        strike_price = calculate_strike(stock.current_price.price(), self._is_itm, self._num_of_strikes, True)
        premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, True)
        new_option = PutOption(stock.symbol, Price(strike_price, stock.current_price.time()), expiration_date, premium)
        return new_option