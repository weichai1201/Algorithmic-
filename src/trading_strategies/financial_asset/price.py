from datetime import datetime


class Price:
    def __init__(self, price: float, timeStamp: datetime):
        self._price = price
        self._timeStamp = timeStamp

    def get_price(self):
        return self._price

    def get_time(self):
        return self._timeStamp