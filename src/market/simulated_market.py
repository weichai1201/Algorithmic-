from src.market.order import Order


class SimulatedMarket:

    @staticmethod
    def submit_order(order: Order):
        order.accept_order()
