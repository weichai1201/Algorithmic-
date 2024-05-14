import datetime
from typing import Set, Dict, List

from src.agent.performance import calculate_option_profit
from src.agent.transactions.transaction import Transaction
from src.data_access.data_package import DataPackage
from src.agent.margins import Margins
from src.market.simulated_market import SimulatedMarket
from src.trading_strategies.financial_asset.financial_asset import FinancialAsset, EmptyAsset
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.calculators.margin_calculator import EquityMarginCalculator
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
        self._assets: Dict[StrategyId, List[FinancialAsset]] = dict()
        self._margins: Dict[StrategyId, Margins] = dict()

    def get_asset(self, strategy_id: StrategyId) -> List[FinancialAsset]:
        if strategy_id not in self._assets.keys():
            return [EmptyAsset()]
        return self._assets[strategy_id]

    def update_asset(self, strategy_id: StrategyId, assets: List[FinancialAsset]):
        self._assets[strategy_id] = assets

    def get_symbols(self) -> Set:
        result: Set[Symbol] = set()
        for strategy in self._strategies.values():
            result.add(strategy.symbol())
        return result

    def update(self, symbol: Symbol, new_data: DataPackage) -> bool:
        # return update is successful or not
        successful = True
        for strategy_id, strategy in self._strategies.items():
            if symbol != strategy.symbol():
                continue

            orders = strategy.update(new_data)
            self._market.submit_order(orders, agent=self, strategy_id=strategy_id)

            if any([not order.is_successful() for order in orders]):
                continue

            # order is successful
            assets = []
            # self.cal_payoff(strategy_id,  ,len(orders))
            for order in orders:
                assets.append(order.asset)
                transaction = Transaction(order.positions, order.asset, order.date, order.msg)
                self._all_transactions[strategy_id].add_transaction(transaction)
            self.update_asset(strategy_id, assets)
            successful = successful & all([order.is_successful() for order in orders])
        return successful

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
            (dates[strategy_id],
             payoffs[strategy_id],
             profits[strategy_id],
             cumulative_profits[strategy_id]) = calculate_option_profit(transactions)
            # drawdowns[strategy_id] = calculate_drawdowns(cumulative_profits[strategy_id])
        return (dates,
                payoffs,
                profits,
                cumulative_profits,
                drawdowns)

    def cal_payoff(self, strategy_id: StrategyId, stock_price: float, num_t=1):
        for t in self._all_transactions[strategy_id].last_n(num_t):
            payoff = t.get_asset().option_payoff(stock_price)
            t.realise_payoff(payoff)
            t.append_msg(f"Realised payoff: {payoff}.\n")

    def notified_margin_update(self, symbol: Symbol, stock_price: float, date: datetime, new_transaction=False):
        for strategy_id, strategy in self._strategies.items():
            if strategy.is_same_symbol(symbol):
                if strategy_id not in self._assets.keys():
                    continue
                assets = self._assets[strategy_id]
                margin = EquityMarginCalculator().calculate_margin(stock_price, assets)
                if strategy_id not in self._margins.keys():
                    self._margins[strategy_id] = Margins()
                self._margins[strategy_id].append_margin(date, margin, new_transaction)

    def get_margins(self):
        return self._margins
