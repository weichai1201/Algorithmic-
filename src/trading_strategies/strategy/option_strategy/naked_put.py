from datetime import datetime, timedelta
from typing import List, Dict, Optional

from src.trading_strategies.financial_asset.option import Option, PutOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.option_pricing import implied_t_put, bsm_pricing
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike, roll_down_strike, \
    get_strike_gap
from src.trading_strategies.strategy.option_strategy.strike_spec import StrikeSpec
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.trading_strategies.transactions.positions import Positions
from src.trading_strategies.transactions.transaction import Transaction
from src.util.expiry_date import next_expiry_date, closest_expiration_date, asx_calendar

risk_free_rate = 0.03

class NakedPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: List[Option], is_itm: bool,
                 is_weekly: bool, weekday="THU", num_of_strikes = 1, scale=1):
        super().__init__(strategy_id, options, scale)
        self._consecutive_itm = 0
        self._num_of_strikes = num_of_strikes
        self._is_weekly = is_weekly
        self._weekday = weekday
        self._is_itm = is_itm

    def in_the_money(self, stock_price: float) -> bool:
        return any([option.in_the_money(stock_price) for option in self._options])

    def itm_amount(self, stock_price: float) -> [float]:
        return [option.itm_amount(stock_price) for option in self._options]

    def roll_over(self):
        """
        Initialisation and expiry with OTM.
        :param price: stock price.
        :param itm_or_otm: set the strike price relatively greater or less than stock price.
        :param premium: the price of the option
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        current_option = self._options[0]
        positions = Positions(Position.SHORT, self._scale)

        return Transaction(positions, current_option, current_option.get_expiry())  # timezone maybe a problem

    def roll_down(self):
        """
        When the option is itm, roll down the next strike price based on current one
        :param num_strikes:
        :param premium:
        :param stock_price:
        :param implied_time:
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        # request the following
        current_option = self._options[0]
        positions = Positions(Position.SHORT, self._scale)

        return Transaction(positions, current_option, current_option.get_expiry())

    def roll_up(self):
        return

    def roll(self, new_option, current_time) -> Optional[Transaction]:
        self._options[0] = new_option
        positions = Positions(Position.SHORT, self._scale)
        return Transaction(positions, new_option, current_time)

    def update(self, new_stock: Stock) -> Optional[Option]:
        stock = new_stock
        current_time = stock.current_price.time()
        stock_price = stock.current_price.price()
        option = self._options[0]

        if not option.is_expired(current_time):
            return None

        if option.in_the_money(stock_price):
            return self._update_itm_option(stock, current_time, option)
        else:
            return self._update_otm_option(stock, current_time)

    def _update_itm_option(self, stock: Stock, current_time: datetime, option: Option) -> Option:
        stock_price = stock.current_price.price()
        premium = option.itm_amount(stock_price) + get_strike_gap(stock_price)
        strike_price = roll_down_strike(stock_price, option.get_strike().price(), self._num_of_strikes)
        implied_time = implied_t_put(stock_price, strike_price, risk_free_rate, premium, stock.garch_long_run)
        new_expiration = closest_expiration_date(current_time + timedelta(days=implied_time * 365), asx_calendar)
        strike = Price(strike_price, new_expiration)
        new_option = PutOption(stock.symbol, strike, new_expiration, premium)
        return new_option

    def _update_otm_option(self, stock: Stock, current_time: datetime) -> Option:
        self._consecutive_itm = 0
        expiration_date = next_expiry_date(current_time, self._weekday, self._is_weekly)
        strike_price = calculate_strike(stock.current_price.price(), self._is_itm, self._num_of_strikes, True)
        premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, False)
        new_option = PutOption(stock.symbol, Price(strike_price, current_time), expiration_date, premium)
        return new_option




