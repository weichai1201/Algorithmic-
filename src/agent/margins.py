from datetime import datetime
from typing import List, Tuple, Dict

import pandas as pd


class Margins:
    def __init__(self):
        self._margins: List[Tuple[datetime, float]] = list()

    def append_margin(self, date: datetime, margin: float):
        self._margins.append(tuple((date, margin)))

    def get_margins(self):
        return self._margins

    def to_dataframe(self):
        return pd.DataFrame(self._margins, columns=["Date", "Margin"])

