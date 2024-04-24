from datetime import datetime
from typing import List, Dict, Optional

from src.data_access.data_access import retrieve_rf
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
from src.util.util import match_strike


class NakedPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: List[Option], specs: [StrikeSpec],
                 is_weekly: bool, weekday="THU", num_of_strikes=1, scale=1):
        super().__init__(strategy_id, options, specs, scale)
        self._consecutive_itm = 0
        self._num_of_strikes = num_of_strikes
        self._is_weekly = is_weekly
        self._weekday = weekday

    def in_the_money(self, stock_price: float) -> bool:
        return any([option.in_the_money(stock_price) for option in self._options])

    def itm_amount(self, stock_price: float) -> [float]:
        return [option.itm_amount(stock_price) for option in self._options]

    def _roll_over(self, stock_price: float, premiums: Dict[float, float], itm_side=True):
        """
        Initialisation and expiry with OTM.
        :param stock_price: stock price.
        :param itm_side: set the strike price relatively greater or less than stock price.
        :param premium: the price of the option
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        # roll over price
        target_strike = calculate_strike(stock_price, itm_side, self._num_of_strikes, True)
        strike, premium = match_strike(target_strike, premiums)

        # construct the new option transaction
        positions = Positions(Position.SHORT, self._scale)
        next_expiry = next_expiry_date(self._options[0].get_expiry(), self._weekday, self._is_weekly)
        option = PutOption(self.symbol(), strike, next_expiry, premium)

        return Transaction(positions, option, self._options[0].get_expiry())  # timezone maybe a problem

    def _roll_down(self, stock_price: float, premiums: Dict[float, float]):
        """
        When the option is itm, roll down the next strike price based on current one
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        option = self._options[0]
        target_strike = roll_down_strike(stock_price, option.get_strike().price(), self._num_of_strikes)
        strike, premium = match_strike(target_strike, premiums)
        rf = retrieve_rf(option.get_expiry().date())
        implied_time = implied_t_put(stock_price, target_strike, rf, premium, 0.04)
        # request the following
        positions = Positions(Position.SHORT, self._scale)
        option = PutOption(self.symbol(), strike, implied_time, premium)
        return Transaction(positions, option, self._options[0].get_expiry())

    def _roll_up(self):
        return

    def update(self, new_data: NewData, time: datetime) -> Optional[Transaction]:
        """
        :param new_data: a tuple of prices (stock_price, dict(strike -> premium)).
        First entry is stock price. Second entry is a dictionary, strike price mapped to premium.
        :return:
        """
        stock_price, premiums = new_data

        if len(self._options) == 0:
            return self._roll_over(stock_price, premiums, True)

        current_time = stock_price
        option = self._options[0]
        if not option.is_expired(current_time):
            return None

        if option.in_the_money(stock_price):
            self._consecutive_itm += 1
            return self._roll_down(stock_price, premiums)
        else:
            # reset the count of itm
            self._consecutive_itm = 0
            return self._roll_over(stock_price, premiums, True)
