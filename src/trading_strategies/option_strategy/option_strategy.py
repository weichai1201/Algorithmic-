from abc import abstractmethod

from src.trading_strategies.strategy.strategy_id import StrategyId


class OptionStrategy:
    @abstractmethod
    def __init__(self, id: StrategyId):
        self.id = id
        self.__dict = {}
        self.__transactions = []

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def execute_strategy(self):
        # Execute strategy
        pass

    @abstractmethod
    def expiration_actions(self):
        # Define actions to take at expiration based on option status
        pass

    @abstractmethod
    def margin_actions(self):
        pass

    @abstractmethod
    def get_id(self):
        pass


class NakedPut(OptionStrategy):
    def execute_strategy(self):
        # Execute strategy for naked put
        pass

    def expiration_actions(self):
        # Define actions to take at expiration for naked put
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
