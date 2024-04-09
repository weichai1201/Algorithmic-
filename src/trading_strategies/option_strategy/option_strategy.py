import datetime
from abc import abstractmethod

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.option import Option, PutOption
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_strategy.spec import Spec
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.positions import ShortPositions
from src.trading_strategies.transactions.transaction import Transaction
from src.util import exception


class OptionStrategy:

    @abstractmethod
    def __init__(self, id: StrategyId, options: [Option], specs: [Spec], scale=1):
        self._id = id
        self._options = options
        self._specs = specs
        self._scale = scale
        self._transactions = []
        self._profits = []  # realised profits for each transactions
        self._current_profit = 0  # reset when option expired and renewed, updated with stock price
        self._cumulative_profit = 0  # updated after positions closed (or option expired)

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
        return self._id

    def get_symbol(self) -> Symbol:
        if len(self._options) == 0:
            return Symbol("")
        return self._options[0].get_symbol()

    def _peek_transaction(self):
        """
        :return: Last transaction if any. Catch index-out-of-bound but do nothing.
        """
        index = len(self._transactions) - 1
        if index < 0:
            exception.ExceptionHandler.raise_index_out_of_range("transactions", index)
        return self._transactions[index]

    @staticmethod
    def _calculate_profit(premium: float, stock_price: float, strike_price: float, quantity) -> float:
        payoff = max(0.0, strike_price - stock_price)
        profit = (premium + payoff * 100) * quantity  # each option respond to 100 shares
        return profit


class NakedPut(OptionStrategy):
    def __init__(self, strategy_id: StrategyId, options: [PutOption], specs: [Spec], scale=1):
        super().__init__(strategy_id, options, specs, scale)

    def __short_put(self):
        """
        assume it is rolling again
        """
        option = self._options[0]
        quantity = self._scale
        transaction = Transaction(ShortPositions(quantity), option, datetime.datetime.now())
        # may require setting timezone as trading in the u.s. while user in au
        self._transactions.append(transaction)
        self._current_profit = option.get_premium() * quantity

    def update(self, new_option: FinancialAsset):
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
