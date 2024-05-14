from datetime import datetime
from typing import List, Tuple, Dict

import pandas as pd


class Margins:
    def __init__(self):
        self._margins: List[Tuple[datetime, float]] = list()

    def append_margin(self, date: datetime, margin: float, new_transaction=False):
        if not new_transaction:
            margin = max(margin, self._get_last_margin())
        self._margins.append(tuple((date, margin)))

    def _get_last_margin(self):
        if len(self._margins) == 0:
            return 0
        return self._margins[len(self._margins) - 1][1]

    def get_margins(self):
        return self._margins

    def to_dataframe(self):
        return pd.DataFrame(self._margins, columns=["Date", "Margin"])

    def max_margin(self):
        return max(x[1] for x in self._margins)
