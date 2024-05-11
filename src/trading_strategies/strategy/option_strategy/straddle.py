from datetime import datetime
from typing import List, Dict

from src.data_access.data_package import DataPackage
from src.market.order import Order, EmptyOrder
from src.trading_strategies.financial_asset.option import Option, EmptyOption, PutOption, CallOption
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.long_call import LongCall
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.strategy_id import StrategyId


class Straddle(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, is_weekly: bool,
                 weekday, num_of_strikes: int, scale=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes)
        self._strategy_call = LongCall(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes, scale)
        self._strategy_put = LongCall(strategy_id, symbol, is_itm, is_weekly, weekday, num_of_strikes, scale)
        self._option_call = EmptyOption()
        self._option_put = EmptyOption()

    def need_update(self, date: datetime):
        if isinstance(self._option_call, EmptyOption) or isinstance(self._option_put, EmptyOption):
            return True
        return any([self._option_call.is_expired(date), self._option_put.is_expired(date)])

    def update(self, new_data: DataPackage) -> List[Order]:
        # unpack data package
        orders = list()
        orders.append(self._strategy_put.update(new_data))
        orders.append(self._strategy_call.update(new_data))
        return orders

    def update_order(self, orders: List[Order]):
        if len(orders) == 0 or not all([x.is_successful() for x in orders]):
            return
        if len(orders) != 2:
            print("Expect to have exactly 2 orders.")
            return
        call_updated = False
        put_updated = False
        for order in orders:
            option = order.asset
            if not isinstance(option, Option):
                print(f"Expect to receive option in straddle {self.id()}.\n")
            if isinstance(option, CallOption):
                self._option_call = option
                call_updated = True
            if isinstance(option, PutOption):
                self._option_put = option
                put_updated = True
        if not all([call_updated, put_updated]):
            print(f"Some option(s) is not updated in straddle {self.id()}.\n")
