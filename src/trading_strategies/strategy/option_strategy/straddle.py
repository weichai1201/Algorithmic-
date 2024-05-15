from datetime import datetime
from typing import List, Dict

from src.agent.transactions.position import Position
from src.agent.transactions.positions import Positions
from src.data_access.data_package import DataPackage
from src.market.order import Order, EmptyOrder
from src.trading_strategies.financial_asset.financial_asset import EmptyAsset
from src.trading_strategies.financial_asset.option import Option, EmptyOption, PutOption, CallOption
from src.trading_strategies.financial_asset.price import Price, EmptyPrice
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.short_call import ShortCall
from src.trading_strategies.strategy.option_strategy.short_put import ShortPut
from src.trading_strategies.strategy.strategy_id import StrategyId


class Straddle(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, is_weekly: bool,
                 weekday, num_of_strikes: int, scale=1, cross_over=True, same_expiration=True,
                 is_itm2=True, is_weekly2=True, num_of_strikes2=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes)
        self._strategy_call = ShortCall(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes, scale, self)
        self._strategy_put = ShortPut(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes, scale, self)
        self._position = Position.SHORT
        self._cross_over = cross_over
        self._same_expiration = same_expiration

    def register_agent(self, agent):
        self._strategy_call.register_agent(agent)
        self._strategy_put.register_agent(agent)
        super().register_agent(agent)

    def get_option_down(self, child: OptionStrategy):
        options = self.current_options()
        if id(child) == id(self._strategy_put):
            for option in options:
                if isinstance(option, PutOption):
                    return option
        if id(child) == id(self._strategy_call):
            for option in options:
                if isinstance(option, CallOption):
                    return option
        return EmptyOption()

    def need_update(self, date: datetime):
        options = self.current_options()
        if any([isinstance(option, EmptyOption) or isinstance(option, EmptyAsset) for option in options]):
            return True
        return any([option.is_expired(date) for option in options])

    def update(self, new_data: DataPackage) -> List[Order]:
        # unpack data package
        date = new_data.date
        orders = self._strategy_put.update(new_data) + self._strategy_call.update(new_data)
        strikes = []
        expirations = []
        for order in orders:
            if isinstance(order, EmptyOrder):
                return [EmptyOrder()]
            if isinstance(order.asset, Option):
                strikes.append(order.asset.get_strike().price())
                expirations.append(order.asset.get_expiry())
        if self._cross_over and strikes[0] > strikes[1]:
            strikes[0] = strikes[1]
        if self._same_expiration:
            expirations[0] = max(expirations)
            expirations[1] = max(expirations)
        msg = "\n".join([o.msg for o in orders])
        put = PutOption(self.symbol(), Price(strikes[0], date), expirations[0], EmptyPrice())
        call = CallOption(self.symbol(), Price(strikes[1], date), expirations[1], EmptyPrice())

        return [Order(put, date, Positions(self._position, self._scale)),
                Order(call, date, Positions(self._position, self._scale), msg)]
