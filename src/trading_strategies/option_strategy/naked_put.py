from src.trading_strategies.financial_asset.option import PutOption
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.transaction import Transaction


class NakedPut():
    def __init__(self, id: StrategyId, option: PutOption, scale):
        super().__init__(id)
        self.__option = option
        self.__scale = scale
        self.__transactions = [Transaction]

    def get_symbol(self):
        return self.__option.get_symbol()

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
        pass
