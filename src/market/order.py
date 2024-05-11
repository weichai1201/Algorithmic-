from datetime import datetime

from src.agent.transactions.position import Position
from src.agent.transactions.positions import Positions
from src.market.order_task import OrderTask
from src.trading_strategies.financial_asset.financial_asset import FinancialAsset


class Order:

    def __init__(self, asset: FinancialAsset, date: datetime, positions: Positions, msg=""):
        self.asset = asset
        self.date = date
        self.positions = positions
        self.msg = msg
        self._task = OrderTask()

    def is_complete(self):
        return self._task.is_complete()

    def is_successful(self):
        return self._task.is_successful()

    def accept_order(self):
        self._task.complete()

    def reject_order(self):
        self._task.complete(result=False)

    def symbol(self):
        return self.asset.symbol()


class EmptyOrder(Order):
    def __init__(self, asset: FinancialAsset):
        super().__init__(asset, datetime.now(), Positions(Position.LONG, 0))
