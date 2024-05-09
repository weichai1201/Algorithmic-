from datetime import datetime

from src.market.order_task import OrderTask
from src.trading_strategies.financial_asset.financial_asset import FinancialAsset


class Order:

    def __init__(self, asset: FinancialAsset, date: datetime, quantity=1.0, ask=0.0, bid=0.0):
        self.asset = asset
        self.date = date
        self.quantity = quantity
        self.ask = ask
        self.bid = bid
        if self.ask > 0:
            self.is_ask = True
        else:
            self.is_ask = False
        self._task = OrderTask()

    def is_complete(self):
        return self._task.is_complete()

    def is_successful(self):
        return self._task.is_successful()

    def accept_order(self):
        self._task.complete()

    def reject_order(self):
        self._task.complete(False)

    def symbol(self):
        return self.asset.symbol()


class EmptyOrder(Order):
    def __init__(self, asset: FinancialAsset):
        super().__init__(asset)