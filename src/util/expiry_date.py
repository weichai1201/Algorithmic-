from datetime import datetime, timedelta


def next_date(date: datetime, next_day):
    days_until_weekday = (weekday_mapping[next_day.upper()] - date.weekday()) % 7
    next_weekday = date + timedelta(days=days_until_weekday)

    return next_weekday.strftime('%Y-%m-%d')

weekday_mapping = {
    'MON': 0,
    'TUE': 1,
    'WED': 2,
    'THU': 3,
    'FRI': 4,
    'SAT': 5,
    'SUN': 6
}