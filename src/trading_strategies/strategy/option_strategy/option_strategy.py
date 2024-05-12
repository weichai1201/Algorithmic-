from abc import abstractmethod
from datetime import datetime
from typing import List, Callable

from src.agent.transactions.position import Position
from src.agent.transactions.positions import Positions
from src.data_access.data_package import DataPackage
from src.data_access.volatility import Volatility
from src.market.order import Order
from src.trading_strategies.financial_asset.financial_asset import EmptyAsset, FinancialAsset
from src.trading_strategies.financial_asset.option import Option, CallOption, EmptyOption, PutOption
from src.trading_strategies.financial_asset.price import EmptyPrice, Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.calculators.option_strike import get_strike_gap
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.util.expiry_date import next_expiry_date

risk_free_rate = 0.03


class OptionStrategy(Strategy):

    @abstractmethod
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol)
        self._id = strategy_id
        self._scale = scale
        self._num_of_strikes = num_of_strikes
        self._is_weekly = is_weekly
        self._weekday = weekday
        self._is_itm = is_itm
        self._position = Position.EMPTY

    def get_id(self) -> StrategyId:
        return self._id

    def notify_agent(self, information: (StrategyId, float)):
        self._agent.realise_payoff(information)

    def current_option(self) -> Option:
        if self._agent is None:
            return EmptyOption()
        return self._agent.get_asset(self._id)

    @staticmethod
    def in_the_money(stock_price: float, option: Option) -> bool:
        return option.in_the_money(stock_price)

    def deep_in_the_money(self, stock_price: float, option: Option) -> bool:
        return self.itm_amount(stock_price, option) > 5 * get_strike_gap(stock_price)

    @staticmethod
    def itm_amount(stock_price: float, option: Option) -> float:
        return option.itm_amount(stock_price)

    def update(self, new_data: DataPackage) -> List[Order]:
        # unpack information
        date = new_data.date
        stock_price = new_data.stock.get_price().price()
        option = self.current_option()
        symbol = option.symbol()
        action: Callable
        msg = ""
        if isinstance(option, EmptyOption):
            action = self.roll_over
            msg = "Instantiate first option by rolling over."
        elif self.in_the_money(stock_price, option):
            if self.deep_in_the_money(stock_price, option):
                action = self._update_deep_itm_option
                msg = "Roll over as deep in the money."
            else:
                action = self._update_mod_itm_option
                msg = "roll up/down as in the money."
        else:
            action = self._update_otm_option
            msg = "Roll over as out of moeny."
        strike, expiry = action(stock_price, date, option)
        if isinstance(option, CallOption):
            next_option = CallOption(symbol, Price(strike, date), expiry, EmptyPrice())
        else:   # put option
            next_option = PutOption(symbol, Price(strike, date), expiry, EmptyPrice())
        order = Order(next_option, date, Positions(self._position, self._scale), msg)
        return [order]

    def _update_mod_itm_option(self, stock_price: float, date: datetime, prev_option: Option) -> (float, datetime):
        if isinstance(prev_option, CallOption):
            return self.roll_up(stock_price, date, prev_option)
        else:
            return self.roll_down(stock_price, date, prev_option)

    def _update_deep_itm_option(self, stock_price: float, date: datetime, prev_option=None) -> (float, datetime):
        return self._update_otm_option(stock_price, date)

    def _update_otm_option(self, stock_price: float, date: datetime, prev_option=None) -> (float, datetime):
        expiration_date = next_expiry_date(date, self._is_weekly, True, self._weekday)
        return self.roll_over(stock_price, expiration_date)

    @abstractmethod
    def roll_over(self, stock_price: float, date: datetime, prev_option=None) -> (float, datetime):
        pass

    @abstractmethod
    def roll_up(self, stock_price: float, date: datetime, prev_option: Option) -> (float, datetime):
        pass

    @abstractmethod
    def roll_down(self, stock_price: float, date: datetime, prev_option: Option) -> (float, datetime):
        pass
