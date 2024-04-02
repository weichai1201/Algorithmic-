from src.trading_strategies.optionStrategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.strategy_id import StrategyId


class NakedPut(OptionStrategy):
    def __init__(self, id: StrategyId):
        super().__init__(id)


    def update(self):
        pass

    def execute_strategy(self):
        pass

    def expiration_actions(self):
        pass

    def margin_actions(self):
        pass

    def get_id(self):
        pass
