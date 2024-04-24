from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.transaction import Transaction


class Transactions:

    def __init__(self, strategy_id: StrategyId):
        self._id = strategy_id
        self._transactions = list[Transaction]()

    def get_id(self):
        return self._id

    def same_id(self, strategy_id: StrategyId):
        return self._id == strategy_id

    def add_transaction(self, transaction: Transaction):
        self._transactions.append(transaction)
