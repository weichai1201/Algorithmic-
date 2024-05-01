from src.trading_strategies.transactions.position import Position

"""
@author: Yifan Xiao
@author: Huanjie Zhang
"""
class Positions:
    def __init__(self, position: Position, quantity: int):
        self.position = position
        self.quantity = quantity

    def __str__(self):
        return self.position.__str__() + " " + str(self.quantity)


class ShortPositions(Positions):
    def __init__(self, quantity: int):
        super().__init__(Position.SHORT, quantity)


class LongPositions(Positions):
    def __init__(self, quantity: int):
        super().__init__(Position.LONG, quantity)
