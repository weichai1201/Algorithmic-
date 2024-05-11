from datetime import datetime


class BacktestingConfig:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date


class OptionBacktestingConfig(BacktestingConfig):

    def __init__(self, start_date=datetime(year=2006, month=1, day=1), end_date=datetime(year=2022, month=1, day=1),
                 is_itm=True, is_weekly=True, num_of_strikes=1, weekday="FRI"):
        super().__init__(start_date, end_date)
        self.is_itm = is_itm
        self.is_weekly = is_weekly
        self.num_of_strikes = num_of_strikes
        self.weekday = weekday


class ShortBacktestingConfig(OptionBacktestingConfig):
    def __init__(self, start_date=datetime(year=2008, month=1, day=1),
                 end_date=datetime(year=2010, month=1, day=1)):
        super().__init__(start_date, end_date)
