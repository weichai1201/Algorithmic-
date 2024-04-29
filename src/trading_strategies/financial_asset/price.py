from datetime import datetime


class Price:
    def __init__(self, price: float, time_stamp: datetime):
        self._price = price
        self._time_stamp = time_stamp

    def price(self):
        return self._price

    def time(self):
        return self._time_stamp

    def __str__(self):
        return str(self._price)
