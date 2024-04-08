from abc import abstractmethod

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import Option
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_strategy.spec import Spec
from src.trading_strategies.strategy.strategy_id import StrategyId


class OptionStrategy:
    @abstractmethod
    def __init__(self, id: StrategyId, specs: {Option, Spec}, scale=1):
        self.__id = id
        self.__specs = specs
        self.__scale = scale
        self.__transactions = []

    @abstractmethod
    def update(self):
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
        for option, spec in self.__specs:
            if option is not None:
                return option.get_symbol()
        return Symbol("")


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
