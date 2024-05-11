from datetime import datetime


class BacktestingConfig:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date


class OptionBacktestingConfig(BacktestingConfig):

    def __init__(self, start_date: datetime, end_date: datetime,
                 is_itm=True, is_weekly=True, num_of_strikes=1, weekday="FRI"):
        super().__init__(start_date, end_date)
        self.is_itm = is_itm
        self.is_weekly = is_weekly
        self.num_of_strikes = num_of_strikes
        self.weekday = weekday
