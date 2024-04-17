class Order:

    def __init__(self, asset: FinancialAsset, ask=0.0, bid=0.0):
        self.asset = asset
        self.ask = ask
        self.bid = bid
        if self.ask > 0:
            self.is_ask = True
        else:
            self.is_ask = False
        self._task = OrderTask()

    def is_complete(self):
        return self._task.is_complete()


