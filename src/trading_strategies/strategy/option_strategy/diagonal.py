from datetime import datetime
from typing import List

from src.agent.transactions.position import Position
from src.agent.transactions.positions import Positions
from src.data_access.data_package import DataPackage
from src.market.order import Order, EmptyOrder
from src.trading_strategies.financial_asset.financial_asset import EmptyAsset
from src.trading_strategies.financial_asset.option import EmptyOption, PutOption, Option
from src.trading_strategies.financial_asset.price import Price, EmptyPrice
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.calculators.margin_calculator import MarginType
from src.trading_strategies.strategy.option_strategy.long_put import LongPut
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.short_put import ShortPut
from src.trading_strategies.strategy.strategy_id import StrategyId


class Diagonal(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, is_weekly: bool,
                 weekday, num_of_strikes: int, scale=1, cross_over=True, same_expiration=True,
                 is_itm_long=True, is_weekly_long=False, num_of_strikes_long=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes)
        self._short_put = ShortPut(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes, scale, self)
        self._long_put = LongPut(strategy_id, symbol, is_itm_long, is_weekly_long, weekday, num_of_strikes_long, scale,
                                 self)
        self._position_short = Position.SHORT
        self._position_long = Position.LONG
        self.margin_type = MarginType.SPREAD

    def register_agent(self, agent):
        self._short_put.register_agent(agent)
        self._long_put.register_agent(agent)
        super().register_agent(agent)

    def need_update(self, date: datetime):
        short_option = self._short_put.current_option()
        long_option = self._long_put.current_option()
        if (isinstance(short_option, EmptyOption) or isinstance(short_option, EmptyAsset) or
                isinstance(long_option, EmptyOption) or isinstance(long_option, EmptyAsset)):
            return True
        return any([option.is_expired(date) for option in (short_option, long_option)])

    def update(self, new_data: DataPackage) -> List[Order]:
        # unpack data package
        date = new_data.date
        orders = self._short_put.update(new_data) + self._long_put.update(new_data)
        strikes = []
        expirations = []
        for order in orders:
            if isinstance(order, EmptyOrder):
                return [EmptyOrder()]
            if isinstance(order.asset, Option):
                strikes.append(order.asset.get_strike().price())
                expirations.append(order.asset.get_expiry())

        msg = "\n".join([o.msg for o in orders])
        short_put = PutOption(self.symbol(), Price(strikes[0], date), expirations[0], EmptyPrice())
        long_put = PutOption(self.symbol(), Price(strikes[1], date), expirations[1], EmptyPrice())

        return [Order(short_put, date, Positions(self._position_short, self._scale), self._short_put.asset_name),
                Order(long_put, date, Positions(self._position_long, self._scale), self._long_put.asset_name, msg)]
