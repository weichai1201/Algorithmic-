from datetime import datetime
from enum import Enum


class VolatilityType(Enum):
    GARCH = "Garch"
    SIMPLE = "Standard_Deviation"

    def __hash__(self):
        self.value.__hash__()


class Volatility:

    def __init__(self, value: float, volatility_type: VolatilityType, start_date: datetime, end_date: datetime):
        self.value = value
        self.type = volatility_type
        self.start_date = start_date
        self._end_date = end_date

    def __hash__(self):
        self.value.__hash__() + self.type.__hash__() + self.start_date.__hash__() + self._end_date.__hash__()
