from datetime import datetime, timedelta

import pandas as pd
from pandas_market_calendars import get_calendar

asx_calendar = get_calendar('ASX')
nyse_calendar = get_calendar('XNYS')


def next_week_expiry(date: datetime, weekday: str):
    days_until_weekday = (weekday_mapping[weekday.upper()] - date.weekday()) % 7
    next_expire_date = date + timedelta(days=days_until_weekday)

    return next_expire_date


def next_month_expiry(date: datetime, weekday: str, ref_week_num=3):
    first_day_next_month = datetime(date.year if date.month != 12 else date.year + 1, (date.month % 12) + 1, 1)
    days_to_add = (weekday_mapping[weekday.upper()] - first_day_next_month.weekday() + 7) % 7 + (ref_week_num - 1) * 7
    next_expire_date = first_day_next_month + timedelta(days=days_to_add)

    return next_expire_date


def next_expiry_date(date: datetime, weekday: str, is_weekly: bool, is_us=True) -> datetime:
    """
    :param date: current date.
    :param weekday: day of the week as three-letter string.
    :param is_weekly: weekly expiry if true; monthly expiry if false.
    :param is_us: using the U.S. calendar, else Australian calendar.
    :return: next expiry date `datetime`.

    @author: Yifan Xiao
    """

    calendar = nyse_calendar if is_us else asx_calendar

    if is_weekly:
        next_us_date = next_week_expiry(date, weekday)
    else:
        next_us_date = next_month_expiry(date, weekday)

    if calendar.valid_days(start_date=next_us_date, end_date=next_us_date).size > 0:
        next_trading_day = next_us_date
    else:
        next_trading_day = calendar.valid_days(start_date=next_us_date, end_date=next_us_date + pd.Timedelta(days=10))[
            0]

    return next_trading_day.replace(tzinfo=None)


weekday_mapping = {
    'MON': 0,
    'TUE': 1,
    'WED': 2,
    'THU': 3,
    'FRI': 4,
    'SAT': 5,
    'SUN': 6
}
