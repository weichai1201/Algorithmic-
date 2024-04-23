from datetime import datetime
from typing import List

from src.trading_strategies.financial_asset.option import Option, PutOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.option_pricing import implied_t_put
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike
from src.trading_strategies.strategy.option_strategy.strike_spec import StrikeSpec
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.trading_strategies.transactions.positions import Positions
from src.trading_strategies.transactions.transaction import Transaction
from src.util.expiry_date import next_expiry_date


class NakedPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: List[Option], specs: [StrikeSpec], is_weekly: bool, weekday="THU", scale=1):
        super().__init__(strategy_id, options, specs, scale)
        self._consecutive_itm = 0
        self._is_weekly = is_weekly
        self._weekday = weekday

    def in_the_money(self, stock_price: float) -> bool:
        return any([option.in_the_money(stock_price) for option in self._options])

    def itm_amount(self, stock_price: float) -> [float]:
        return [option.itm_amount(stock_price) for option in self._options]

    def roll_over(self, price: float, itm_or_otm: bool, num_strikes: int, premium: Price):
        """
        Initialisation and expiry with OTM.
        :param price: stock price.
        :param itm_or_otm: set the strike price relatively greater or less than stock price.
        :param num_strikes: number of strikes based on strike gap guide, away from stock price.
        :param premium: the price of the option
        :return: `Transaction` order to `Agent`.

        @author: Huanjie Zhang
        """

        current_option = self._options[0]
        strike = calculate_strike(price, itm_or_otm, num_strikes, True)

        # construct the new option transaction
        positions = Positions(Position.SHORT, self._scale)
        next_expiry = next_expiry_date(current_option.get_expiry(), self._weekday, self._is_weekly)
        option = PutOption(self.symbol(), strike, next_expiry, premium)

        return Transaction(positions, option, current_option.get_expiry())  # timezone maybe a problem

    def roll_down(self, price: float, num_strikes: int, implied_time: datetime):
        """
        ITM
        :return:
        """
        pass

    def roll_up(self):
        return

    def update(self, new_data):
        pass

    def expiration_actions(self):
        pass
