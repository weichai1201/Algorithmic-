from typing import List

from src.trading_strategies.financial_asset.option import Option
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.strike_spec import StrikeSpec
from src.trading_strategies.strategy.strategy_id import StrategyId


class NakedPut (OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: List[Option], specs: [StrikeSpec], scale=1):
        super().__init__(strategy_id, options, specs, scale)

    def in_the_money(self, stock_price: float) -> bool:
        return any([option.in_the_money(stock_price) for option in self._options])

    def itm_amount(self, stock_price: float) -> [float]:
        return [option.itm_amount(stock_price) for option in self._options]

    def update(self, new_data):
        pass

    def expiration_actions(self):
        pass

    def margin_actions(self):
        pass
