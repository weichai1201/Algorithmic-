import datetime
from abc import abstractmethod
from typing import List, Dict, Optional

from src.trading_strategies.financial_asset.option import Option, PutOption, CallOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing, implied_date
from src.trading_strategies.strategy.option_strategy.option_strike import get_strike_gap, calculate_strike, \
    roll_down_strike, roll_up_strike
from src.trading_strategies.strategy.option_strategy.strike_spec import StrikeSpec
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.trading_strategies.transactions.positions import Positions
from src.trading_strategies.transactions.transaction import Transaction
from src.util.exception import ExceptionHandler
from src.util.expiry_date import next_expiry_date, closest_expiration_date, nyse_calendar

risk_free_rate = 0.03

class OptionStrategy(Strategy):

    @abstractmethod
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, position: Position,
                 is_weekly: bool, weekday="THU", num_of_strikes=1, scale=1):
        super().__init__(strategy_id, symbol)
        self._id = strategy_id
        self._scale = scale
        self._num_of_strikes = num_of_strikes
        self._is_weekly = is_weekly
        self._weekday = weekday
        self._is_itm = is_itm
        self._positions = Positions(position, scale)

    @abstractmethod
    def in_the_money(self, stock_price: float, option) -> bool:
        return option.in_the_money(stock_price)

    @abstractmethod
    def deep_in_the_money(self, stock_price: float, option) -> bool:
        return self.itm_amount(stock_price, option) > 5 * get_strike_gap(stock_price)

    @abstractmethod
    def itm_amount(self, stock_price: float, option) -> float:
        return option.itm_amount(stock_price)

    # @abstractmethod
    # def update(self, new_data):
    #     pass

    def get_id(self) -> StrategyId:
        return self._id

    def roll(self, new_option: Option) -> Optional[Transaction]:
        return Transaction(self._positions, new_option, new_option.get_strike().time())

    def update(self, new_stock: Stock, option: Option) -> Optional[Transaction]:
        current_time = new_stock.current_price.time()
        stock_price = new_stock.current_price.price()

        if not option.is_expired(current_time):
            if option.get_strike().time() == current_time:
                return Transaction(self._positions, option, current_time)
            else:
                return None

        if self.in_the_money(stock_price, option):
            if self.deep_in_the_money(stock_price, option):
                new_option = self._update_deep_itm_option(new_stock, option)
            else:
                new_option = self._update_mod_itm_option(new_stock, option)
        else:
            new_option = self._update_otm_option(new_stock)

        return Transaction(self._positions, new_option, current_time)

    def _update_otm_option(self, stock) -> Option:
        expiration_date = next_expiry_date(stock.current_price.time(), self._is_weekly, True, self._weekday)
        strike_price = calculate_strike(stock.current_price.price(), self._is_itm, self._num_of_strikes, True)
        premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, False)
        new_option = PutOption(stock.symbol, Price(strike_price, stock.current_price.time()), expiration_date, premium)
        return new_option

    def _update_mod_itm_option(self, stock, option) -> Option:
        premium = option.itm_amount(stock.current_price.price()) + get_strike_gap(stock.current_price.price())
        if isinstance(option, CallOption):
            return self._roll_up(stock, option, premium)
        else:
            return self._roll_down(stock, option, premium)

    def _update_deep_itm_option(self, new_stock, option) -> Option:
        return self._update_otm_option(new_stock)

    def _roll_up(self, stock, option, premium) -> Option:
        strike_price = roll_up_strike(stock.current_price.price(), option.get_strike().price(), self._num_of_strikes)
        new_expiration = implied_date(stock.current_price, strike_price, risk_free_rate, premium,
                                      stock.calculate_garch(), False)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        premium = bsm_pricing(stock, strike_price, new_expiration, [], risk_free_rate, True)
        strike = Price(strike_price, stock.current_price.time())
        new_option = PutOption(stock.symbol, strike, new_expiration, premium)
        return new_option

    def _roll_down(self, stock, option, premium) -> Option:
        strike_price = roll_down_strike(stock.current_price.price(), option.get_strike().price(), self._num_of_strikes)
        new_expiration = implied_date(stock.current_price, strike_price, risk_free_rate, premium,
                                      stock.calculate_garch(), True)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        premium = bsm_pricing(stock, strike_price, new_expiration, [], risk_free_rate, False)
        strike = Price(strike_price, stock.current_price.time())
        new_option = PutOption(stock.symbol, strike, new_expiration, premium)
        return new_option

    @staticmethod
    def _calculate_put_payoff(stock_price: float, strike_price: float):
        # assume long position.
        return max(0.0, strike_price - stock_price)

    @staticmethod
    def _calculate_call_payoff(stock_price: float, strike_price: float):
        # assume long position.
        return max(0.0, stock_price - strike_price)

# class NakedPut(OptionStrategy):
#     def __init__(self, strategy_id: StrategyId, options: List[PutOption], specs: [StrikeSpec], scale=1):
#         super().__init__(strategy_id, options, specs, scale)
#
#     def __short_put(self):
#         """
#         assume it is rolling again. Short sell a new put.
#         """
#         option = self._options[0]
#         quantity = self._scale
#         transaction = Transaction(ShortPositions(quantity), option, datetime.datetime.now())
#         # may require setting timezone as trading in the u.s. while user in au
#         self._transactions.append(transaction)
#         self._current_profit = option.get_premium() * quantity
#
#     def request_option(self, option) -> bool:
#         self.get_id()
#         # assume always able to trade the wanted option at backtesting.
#         # observer interface to senf stock symbol and strike price.
#         return True
#
#     def __terminate_put(self):
#         profit = self._current_profit
#         self._profits.append(profit)
#         self._cumulative_profit += profit
#         self._current_profit = 0
#
#     def update(self, new_option: FinancialAsset) -> Order:
#         pass
#
#     def expiration_actions(self):
#         self.__terminate_put()
#         self.__short_put()
#
#     def margin_actions(self):
#         pass
#
#
# class NakedStraddle(OptionStrategy):
#     def execute_strategy(self):
#         # Execute strategy for naked straddle
#         pass
#
#     def expiration_actions(self):
#         # Define actions to take at expiration for naked straddle
#         pass
#
#
# class DiagonalSpreads(OptionStrategy):
#     def execute_strategy(self):
#         # Execute strategy for diagonal spreads
#         pass
#
#     def expiration_actions(self):
#         # Define actions to take at expiration for diagonal spreads
#         pass
