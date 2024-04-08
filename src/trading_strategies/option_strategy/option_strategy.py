import datetime
from abc import abstractmethod

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import Option, PutOption
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_strategy.spec import Spec
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.positions import ShortPositions
from src.trading_strategies.transactions.transaction import Transaction


class OptionStrategy:
    @abstractmethod
    def __init__(self, id: StrategyId, options: [Option], specs: [Spec], scale=1):
        self.__id = id
        self.__options = options
        self.__specs = specs
        self.__scale = scale
        self.__transactions = []

    @abstractmethod
    def update(self, new_data):
        pass

    # @abstractmethod
    # def execute_strategy(self, option, scale):
    # Execute strategy
    #    pass

    @abstractmethod
    def expiration_actions(self):
        # Define actions to take at expiration based on option status
        pass

    @abstractmethod
    def margin_actions(self):
        pass

    def get_id(self) -> StrategyId:
        return self.__id

    def get_symbol(self) -> Symbol:
        if len(self.__options) == 0:
            return Symbol("")
        return self.__options[0].get_symbol()


class NakedPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: [PutOption], specs: [Spec], scale=1):
        super().__init__(strategy_id, options, specs, scale)

    def __short_put(self):
        transaction = Transaction(ShortPositions(self.__scale), self.__options[0], datetime.datetime.now())
        # may require setting timezone as trading in the u.s. while user in au
        self.__transactions.append(transaction)
        pass

        pass

    def add_transaction(self, transaction: Transaction):
        pass

    def execute_strategy(self):
        pass

    def expiration_actions(self):
        pass

    def margin_actions(self):
        pass


class NakedStraddle(OptionStrategy):
    def execute_strategy(self):
        # Execute strategy for naked straddle
        pass

    def expiration_actions(self):
        # Define actions to take at expiration for naked straddle
        pass


class DiagonalSpreads(OptionStrategy):
    def execute_strategy(self):
        # Execute strategy for diagonal spreads
        pass

    def expiration_actions(self):
        # Define actions to take at expiration for diagonal spreads
        pass
