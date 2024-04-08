from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import PutOption, Option
from src.trading_strategies.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.option_strategy.spec import Spec
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.transaction import Transaction


class NakedPut(OptionStrategy):
    def __init__(self, id: StrategyId, specs: {Option, Spec}):
        super().__init__(id, specs)

    def get_symbol(self):
        self.__specs
        return

    def update(self):
        pass

    def add_transaction(self, transaction: Transaction):
        pass

    def execute_strategy(self):
        pass

    def expiration_actions(self):
        pass

    def margin_actions(self):
        pass

    def get_id(self):
        return self.__i
