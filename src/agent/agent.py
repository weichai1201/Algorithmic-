import datetime
from typing import Set

from src.agent.performance import calculate_option_payoff, calculate_option_profit, calculate_drawdowns
from src.agent.transactions.transaction import Transaction
from src.data_access.data_package import DataPackage
from src.market.simulated_market import SimulatedMarket
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.agent.transactions.transactions import Transactions


class Agent:
    # used in agent-based back testing. Assume to be no agents in simple daily market replay (single agent).
    # -strategies: Map < StrategyId, Strategy >
    # -transactions: Map < StrategyId, Transactions >

    def __init__(self, strategies: dict[StrategyId, Strategy]):
        self._strategies = strategies
        self._all_transactions = dict[StrategyId, Transactions]()
        for strategy_id, strategy in strategies.items():
            self._all_transactions[strategy_id] = Transactions(strategy_id)
            strategy.register_agent(self)
        self._market = SimulatedMarket()

    def get_symbols(self) -> Set:
        result: Set[Symbol] = set()
        for strategy in self._strategies.values():
            result.add(strategy.symbol())
        return result

    def update(self, symbol: Symbol, new_data: DataPackage):
        for strategy_id, strategy in self._strategies.items():
            if symbol == strategy.symbol():
                orders = strategy.update(new_data)
                self._market.submit_order(orders)
                if orders.is_successful():
                    strategy.update_order(orders)
                    transaction = Transaction(orders.positions, orders.asset, orders.date, orders.msg)
                    self._all_transactions[strategy_id].add_transaction(transaction)

    def get_all_transactions(self) -> dict[StrategyId, Transactions]:
        return self._all_transactions

    def need_update(self, date: datetime) -> bool:
        return any([strategy.need_update(date) for strategy in self._strategies.values()])

    def need_update_for(self, date: datetime, symbol: Symbol):
        for strategy in self._strategies.values():
            if strategy.is_same_symbol(symbol):
                if strategy.need_update(date):
                    return True
        return False

    def evaluate(self):
        dates = dict[StrategyId, list[float]]()
        payoffs = dict[StrategyId, list[float]]()
        profits = dict[StrategyId, list[float]]()
        cumulative_profits = dict[StrategyId, list[tuple[float, float]]]()
        drawdowns = dict[StrategyId, list[float]]()

        for strategy_id, transactions in self._all_transactions.items():
            dates[strategy_id] = []
            for transaction in transactions.get_transactions():
                dates[strategy_id].append(transaction.get_time())
            payoffs[strategy_id] = calculate_option_payoff(transactions)[0]
            profits[strategy_id], cumulative_profits[strategy_id] = calculate_option_profit(transactions)
            # drawdowns[strategy_id] = calculate_drawdowns(cumulative_profits[strategy_id])
        return (dates,
                payoffs,
                profits,
                cumulative_profits,
                drawdowns)

    def realise_payoff(self, information: (StrategyId, float)):
        strategy_id, payoff = information
        t = self._all_transactions[strategy_id].peak_last()
        if t is not None:
            t.realise_payoff(payoff)
