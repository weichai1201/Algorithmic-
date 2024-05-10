from abc import abstractmethod
from datetime import datetime

from src.data_access.data_package import DataPackage
from src.trading_strategies.financial_asset.option import Option, CallOption
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.option_strike import get_strike_gap
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

    def notify_agent(self, information: (StrategyId, float)):
        self._agent.realise_payoff(information)

    @abstractmethod
    def update(self, new_data: DataPackage):
        pass

    @abstractmethod
    def roll_over(self, stock: Stock, expiration_date: datetime) -> (float, datetime):
        pass

    @abstractmethod
    def roll_up(self, stock: Stock, option: Option, premium: float) -> (float, datetime):
        pass

    @abstractmethod
    def roll_down(self, stock: Stock, option: Option, premium: float) -> (float, datetime):
        pass

    def get_id(self) -> StrategyId:
        return self._id

    def in_the_money(self, stock_price: float, option: Option) -> bool:
        return option.in_the_money(stock_price)

    def deep_in_the_money(self, stock_price: float, option: Option) -> bool:
        return self.itm_amount(stock_price, option) > 5 * get_strike_gap(stock_price)

    def itm_amount(self, stock_price: float, option: Option) -> float:
        return option.itm_amount(stock_price)

    # def update2(self, stock_price: float, option: Option, date: datetime) -> Optional[Transaction]:
    #     if not option.is_expired(date):
    #         if option.get_strike().time() == date:
    #             return Transaction(self._positions, option, date)
    #         else:
    #             return None
    #     new_stock = Stock(self.symbol(), Price(stock_price, date))
    #     if self.in_the_money(stock_price, option):
    #         if self.deep_in_the_money(stock_price, option):
    #             new_option = self._update_deep_itm_option(new_stock, option)
    #         else:
    #             new_option = self._update_mod_itm_option(new_stock, option)
    #     else:
    #         new_option = self._update_otm_option(new_stock)
    #
    #     return Transaction(self._positions, new_option, date)

    def _update_otm_option(self, stock: Stock) -> Option:
        expiration_date = next_expiry_date(stock.get_price().time(), self._is_weekly, True, self._weekday)
        return self.roll_over(stock, expiration_date)

    def _update_mod_itm_option(self, stock: Stock, option) -> Option:
        premium = option.itm_amount(stock.get_price().price()) + get_strike_gap(stock.get_price().price())
        if isinstance(option, CallOption):
            return self.roll_up(stock, option, premium)
        else:
            return self.roll_down(stock, option, premium)

    def _update_deep_itm_option(self, new_stock, option) -> Option:
        return self._update_otm_option(new_stock)
