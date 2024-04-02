from src.optionStrategy.holding_id import HoldingId


class Holding:
    def __init__(self, id: HoldingId):
        self.id = id
        self.stock_option_strategies = {}