import math


def daily_vol_to_annual(vol: float):
    return vol * math.sqrt(252)