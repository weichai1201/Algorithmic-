import datetime
from typing import Set

from src.backtesting.simulated_market import SimulatedMarket
from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.trading_strategies.transactions.positions import Positions
from src.trading_strategies.transactions.transaction import Transaction
from src.trading_strategies.transactions.transactions import Transactions


class Agent:
    # used in agent-based back testing. Assume to be no agents in simple daily market replay (single agent).
    # -strategies: Map < StrategyId, Strategy >
    # -transactions: Map < StrategyId, Transactions >

    def __init__(self, strategies: dict[StrategyId, Strategy]):
        self._strategies = strategies
        self._transactions = dict[StrategyId, Transactions]()
        for strategy_id in strategies.keys():
            self._transactions[strategy_id] = Transactions(strategy_id)
        pass

    def get_symbols(self):
        result = set[Symbol]()
        for strategy in self._strategies.values():
            result.add(strategy.symbol())
        return result

    def update(self, symbol: Symbol, new_data, time: datetime):
        for strategy_id, strategy in self._strategies.items():
            if symbol == strategy.symbol():
                transaction = strategy.update(new_data, time)
                # SimulatedMarket.submit_order(order)
                # if order.is_successful():
                #     positions: Positions
                #     if order.is_ask:
                #         positions = Positions(Position.SHORT, order.quantity)
                #     else:
                #         positions = Positions(Position.LONG, order.quantity)
                #     transaction = Transaction(positions, order.asset, datetime.datetime.now())
                if transaction is not None:
                    self._transactions.get(strategy_id).add_transaction(transaction)

    def transactions(self):
        return self._transactions

    def need_update(self, date: datetime) -> bool:
        return any([strategy.need_update(date) for strategy in self._strategies.values()])
