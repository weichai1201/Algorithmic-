from datetime import datetime
from typing import Callable


class BacktestConfig:
    def __init__(self, strategy: Callable, start_date: datetime, end_date: datetime):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date


class OptionBacktestConfig(BacktestConfig):

    def __init__(self, strategy: Callable,
                 start_date=datetime(year=2006, month=1, day=1),
                 end_date=datetime(year=2022, month=1, day=1),
                 is_itm=True,
                 is_weekly=True,
                 num_of_strikes=1,
                 weekday="FRI"):
        super().__init__(strategy, start_date, end_date)
        self.is_itm = is_itm
        self.is_weekly = is_weekly
        self.num_of_strikes = num_of_strikes
        self.weekday = weekday

    def __str__(self):
        return (f"Configuration for {self.strategy.__name__}: "
                f"itm={self.is_itm}, "
                f"weekly={self.is_weekly}, "
                f"num_of_strikes={self.num_of_strikes}, "
                f"weekday={self.weekday}."
                )


class ShortBacktestConfig(OptionBacktestConfig):
    def __init__(self, strategy: Callable,  start_date=datetime(year=2008, month=1, day=1),
                 end_date=datetime(year=2010, month=1, day=1)):
        super().__init__(strategy, start_date, end_date)


class OptionBacktestConfigBundle:
    def __init__(self, strategy: Callable):
        self.configs = [OptionBacktestConfig(strategy)]
        self.configs.append(OptionBacktestConfig(strategy, is_itm=False))
        self.configs.append(OptionBacktestConfig(strategy, is_weekly=False))
        self.configs.append(OptionBacktestConfig(strategy, is_itm=False, is_weekly=False))
        self.configs.append(OptionBacktestConfig(strategy, num_of_strikes=2))
