from src.market.order import Order


class MarketSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SimulatedMarket(MetaClass=MarketSingletonMeta):

    def __init__(self):
        self._order_book = []

    def submit_order(self, order: Order):
        order.accept_order()
