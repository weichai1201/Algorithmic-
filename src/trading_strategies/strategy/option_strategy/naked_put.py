from datetime import datetime
from typing import List, Dict, Optional

from src.trading_strategies.financial_asset.option import Option, PutOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.option_pricing import implied_t_put
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy, NewData
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike, roll_down_strike
from src.trading_strategies.strategy.option_strategy.strike_spec import StrikeSpec
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.trading_strategies.transactions.positions import Positions
from src.trading_strategies.transactions.transaction import Transaction
from src.util.expiry_date import next_expiry_date


class NakedPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: List[Option], specs: [StrikeSpec],
                 is_weekly: bool, weekday="THU", num_of_strikes = 1, scale=1):
        super().__init__(strategy_id, options, specs, scale)
        self._consecutive_itm = 0
        self._num_of_strikes = num_of_strikes
        self._is_weekly = is_weekly
        self._weekday = weekday

    def in_the_money(self, stock_price: float) -> bool:
        return any([option.in_the_money(stock_price) for option in self._options])

    def itm_amount(self, stock_price: float) -> [float]:
        return [option.itm_amount(stock_price) for option in self._options]

    def roll_over(self, price: float, itm_or_otm: bool, premium: Price):
        """
        Initialisation and expiry with OTM.
        :param price: stock price.
        :param itm_or_otm: set the strike price relatively greater or less than stock price.
        :param premium: the price of the option
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        current_option = self._options[0]
        strike = calculate_strike(price, itm_or_otm, self._num_of_strikes, True)

        # construct the new option transaction
        positions = Positions(Position.SHORT, self._scale)
        next_expiry = next_expiry_date(current_option.get_expiry(), self._weekday, self._is_weekly)
        option = PutOption(self.symbol(), strike, next_expiry, premium)

        return Transaction(positions, option, current_option.get_expiry())  # timezone maybe a problem

    def roll_down(self, stock_price: float, num_strikes:int, implied_time: datetime, premium: Price):
        """
        When the option is itm, roll down the next strike price based on current one
        :param num_strikes:
        :param premium:
        :param stock_price:
        :param implied_time:
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        # current info
        current_option = self._options[0]
        current_strike = current_option.get_strike()
        # target rolled down strike price
        strike = Price(roll_down_strike(stock_price, current_strike.price(), num_strikes), implied_time)

        # request the following
        positions = Positions(Position.SHORT, self._scale)
        option = PutOption(self.symbol(), strike, implied_time, premium)

        return Transaction(positions, option, current_option.get_expiry())

    def roll_up(self):
        return

    def update(self, new_data: NewData) -> Optional[Transaction]:
        """
        :param new_data: a tuple of prices (stock_price, dict(strike -> premium)).
        First entry is stock price. Second entry is a dictionary, strike price mapped to premium.
        :return:
        """
        stock_price, strikes = new_data

        current_time = stock_price.price
        option = self._options[0]
        if not option.is_expired(current_time):
            return None

        if option.in_the_money(stock_price):
            self._consecutive_itm += 1
            implied_time = datetime

            return self.roll_down(stock_price, self._consecutive_itm, implied_time, premium)
        else:
            self._consecutive_itm = 0
            return self.roll_over(stock_price, )




