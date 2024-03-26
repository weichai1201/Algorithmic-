from datetime import datetime


class Price:
    def __init__(self, price: float, timeStamp: datetime):
        self.price = price
        self.timeStamp = timeStamp