import datetime

from src.agent.performance import calculate_option_payoff, calculate_option_profit, calculate_drawdowns
from src.order.simulated_market import SimulatedMarket
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.transactions import Transactions


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

    def get_symbols(self):
        result = set[Symbol]()
        for strategy in self._strategies.values():
            result.add(strategy.symbol())
        return result

    def update(self, symbol: Symbol, new_data, time: datetime, market=SimulatedMarket()):
        for strategy_id, strategy in self._strategies.items():
            if symbol == strategy.symbol():
                transaction = strategy.update(new_data, time)
                # market.submit_order(order)
                # if order.is_successful():
                #     positions: Positions
                #     if order.is_ask:
                #         positions = Positions(Position.SHORT, order.quantity)
                #     else:
                #         positions = Positions(Position.LONG, order.quantity)
                #     transaction = Transaction(positions, order.asset, datetime.datetime.now())
                if transaction is not None:
                    self._all_transactions.get(strategy_id).add_transaction(transaction)

    def transactions(self):
        return self._all_transactions

    def need_update(self, date: datetime) -> bool:
        return any([strategy.need_update(date) for strategy in self._strategies.values()])

    def evaluate(self):
        payoffs = dict[StrategyId, list[float]]()
        profits = dict[StrategyId, list[float]]()
        cumulative_profits = dict[StrategyId, list[float]]()
        drawdowns = dict[StrategyId, list[float]]()
        for strategy_id, transactions in self._all_transactions.items():
            payoffs[strategy_id] = calculate_option_payoff(transactions)[0]
            profits[strategy_id], cumulative_profits[strategy_id] = calculate_option_profit(transactions)
            drawdowns[strategy_id] = calculate_drawdowns(cumulative_profits[strategy_id])
        return {"payoffs": payoffs,
                "profits": profits,
                "cumulative_profits": cumulative_profits,
                "drawdowns": drawdowns}

    def realise_payoff(self, information: (StrategyId, float)):
        strategy_id, payoff = information
        t = self._all_transactions[strategy_id].peak_last()
        if t is not None:
            t.realise_payoff(payoff)
