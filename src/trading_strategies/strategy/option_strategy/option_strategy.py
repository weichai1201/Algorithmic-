import datetime
from abc import abstractmethod
from typing import List, Dict

from src.trading_strategies.financial_asset.option import Option, PutOption, CallOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.strike_spec import StrikeSpec
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.util.exception import ExceptionHandler

NewData: (float, Dict[float, float])


class OptionStrategy(Strategy):

    @abstractmethod
    def __init__(self, strategy_id: StrategyId, symbol: Symbol, specs: [StrikeSpec], scale=1):
        super().__init__(strategy_id, symbol)
        self._id = strategy_id
        self._options: [Option] = []
        self._specs = specs
        self._scale = scale

    @abstractmethod
    def in_the_money(self, stock_price: float) -> bool:
        pass

    @abstractmethod
    def itm_amount(self, stock_price: float) -> [float]:
        pass

    @abstractmethod
    def update(self, new_data, date: datetime):
        pass

    def get_id(self) -> StrategyId:
        return self._id

    def get_expiry(self) -> [datetime]:
        return [option.get_expiry() for option in self._options]

    def get_payoffs(self, stock_price: float | Price) -> [float]:
        if isinstance(stock_price, Price):
            stock_price = stock_price.price()
        payoffs = []
        for option in self._options:
            if isinstance(option, CallOption):
                payoffs.append(self._calculate_call_payoff(stock_price, option.get_strike()))
            else:
                payoffs.append(self._calculate_put_payoff(stock_price, option.get_strike()))

    @staticmethod
    def _calculate_put_payoff(stock_price: float, strike_price: float):
        # assume long position.
        return max(0.0, strike_price - stock_price)

    @staticmethod
    def _calculate_call_payoff(stock_price: float, strike_price: float):
        # assume long position.
        return max(0.0, stock_price - strike_price)

# class NakedPut(OptionStrategy):
#     def __init__(self, strategy_id: StrategyId, options: List[PutOption], specs: [StrikeSpec], scale=1):
#         super().__init__(strategy_id, options, specs, scale)
#
#     def __short_put(self):
#         """
#         assume it is rolling again. Short sell a new put.
#         """
#         option = self._options[0]
#         quantity = self._scale
#         transaction = Transaction(ShortPositions(quantity), option, datetime.datetime.now())
#         # may require setting timezone as trading in the u.s. while user in au
#         self._transactions.append(transaction)
#         self._current_profit = option.get_premium() * quantity
#
#     def request_option(self, option) -> bool:
#         self.get_id()
#         # assume always able to trade the wanted option at backtesting.
#         # observer interface to senf stock symbol and strike price.
#         return True
#
#     def __terminate_put(self):
#         profit = self._current_profit
#         self._profits.append(profit)
#         self._cumulative_profit += profit
#         self._current_profit = 0
#
#     def update(self, new_option: FinancialAsset) -> Order:
#         pass
#
#     def expiration_actions(self):
#         self.__terminate_put()
#         self.__short_put()
#
#     def margin_actions(self):
#         pass
#
#
# class NakedStraddle(OptionStrategy):
#     def execute_strategy(self):
#         # Execute strategy for naked straddle
#         pass
#
#     def expiration_actions(self):
#         # Define actions to take at expiration for naked straddle
#         pass
#
#
# class DiagonalSpreads(OptionStrategy):
#     def execute_strategy(self):
#         # Execute strategy for diagonal spreads
#         pass
#
#     def expiration_actions(self):
#         # Define actions to take at expiration for diagonal spreads
#         pass
