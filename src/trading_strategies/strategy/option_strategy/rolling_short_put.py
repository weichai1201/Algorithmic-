from datetime import datetime
from typing import List

from src.agent.transactions.positions import Positions
from src.data_access.data_package import DataPackage
from src.market.order import Order, EmptyOrder
from src.trading_strategies.financial_asset.financial_asset import EmptyAsset
from src.trading_strategies.financial_asset.option import Option, EmptyOption, PutOption
from src.trading_strategies.financial_asset.price import Price, EmptyPrice
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.naked_put import NakedPut
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import get_strike_gap
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.agent.transactions.position import Position
from src.util.expiry_date import next_expiry_date


class RollingShortPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, is_weekly: bool,
                 weekday, num_of_strikes: int, scale=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes)
        self._naked_put = NakedPut(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes, scale)
        self._option: Option = EmptyOption()

    def need_update(self, date: datetime):
        if isinstance(self._option, EmptyOption):
            return True
        return self._option.is_expired(date)

    def _require_roll_over(self, stock_price: float):
        if isinstance(self._option, EmptyOption):
            # instantiate the strategy
            return True
        if not self._option.in_the_money(stock_price) or self._option.deep_in_the_money(stock_price):
            # out of money | deep in the money
            return True
        return False

    def update(self, new_data: DataPackage) -> List[Order]:
        new_stock = new_data.stock
        date = new_data.date
        stock_price = new_stock.get_price().price()
        expiry = next_expiry_date(date, self._is_weekly)
        strike: float
        msg = ""
        if isinstance(self._option, EmptyOption):
            # initiate the first roll
            strike = self._naked_put.roll_over(new_stock, expiry)[0]
            msg = "Initiate first option."
        elif not self._option.is_expired(date):
            return [EmptyOrder(EmptyAsset())]
        else:
            self.notify_agent((self.id(), self._option.option_payoff(stock_price)))
            if self._require_roll_over(stock_price):
                strike = self._naked_put.roll_over(new_stock, expiry)[0]
                msg = "Roll over naked short put."
            else:
                # moderately in the money
                premium = self._option.itm_amount(stock_price) + get_strike_gap(stock_price)
                strike, expiry = self._naked_put.roll_down(new_stock, self._option, premium)
                msg = "Roll down naked short put."
        strike_price = Price(strike, date)
        next_option = PutOption(self._symbol, strike_price, expiry, EmptyPrice())
        msg = msg + f" Stock price at {stock_price}."
        order = Order(next_option, date, Positions(Position.SHORT, self._scale), msg)
        return [order]

    def update_order(self, orders: List[Order]):
        if len(orders) == 0 or not all([x.is_successful() for x in orders]):
            return
        if len(orders) > 1:
            print("Expect to have exactly one order only.")
            return
        new_option = orders[0].asset
        if not isinstance(new_option, Option):
            print("Expect to have option in Naked Put Strategy.")
            return
        self._option = new_option

    def roll_over(self, stock, expiration_date) -> Option:
        return self._naked_put.roll_over(stock, expiration_date)

    def roll_up(self, stock, option, premium) -> Option:
        return self._naked_put.roll_up(stock, option, premium)

    def roll_down(self, stock, option, premium) -> Option:
        return self._naked_put.roll_down(stock, option, premium)
