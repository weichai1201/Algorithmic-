from src.order.order import Order


class SimulatedMarket:

    def submit_order(self, order: Order):
        order.accept_order()


