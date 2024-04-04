import datetime
from scipy.stats import norm
import math

from src.trading_strategies.financial_asset.option import Option, CallOption, PutOption
from src.trading_strategies.financial_asset.stock import Stock
import src.util.util as util

"""
@:param volatility: annual
@:param risk free rate: continuous
"""


def bsm_pricing(stock: Stock, option: Option, risk_free_rate):
    time_to_maturity = (option.get_expire() - stock.current_price.timeStamp) / datetime.timedelta(days=365)
    volatility = util.daily_vol_to_annual(stock.volatility)
    if isinstance(option, CallOption):
        return calculate_call_price(stock.current_price.price, option.get_strike().price,
                                    volatility, time_to_maturity, risk_free_rate)
    elif isinstance(option, PutOption):
        return calculate_put_price(stock.current_price.price, option.get_strike().price,
                                   volatility, time_to_maturity, risk_free_rate)
    else:
        raise ValueError("Invalid option type")


def calculate_call_price(stock_price, strike_price, volatility, time_to_maturity, risk_free_rate):
    d1 = calculate_d1(stock_price, volatility, strike_price, time_to_maturity, risk_free_rate)
    d2 = calculate_d2(d1, volatility, time_to_maturity)
    call_price = stock_price * norm.cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
    return call_price


def calculate_put_price(stock_price, strike_price, volatility, time_to_maturity, risk_free_rate):
    d1 = calculate_d1(stock_price, volatility, strike_price, time_to_maturity, risk_free_rate)
    d2 = calculate_d2(d1, volatility, time_to_maturity)
    put_price = strike_price * math.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - stock_price * norm.cdf(
        -d1)
    return put_price


def calculate_d1(stock_price, volatility, strike_price, time_to_maturity, risk_free_rate):
    return (math.log(stock_price / strike_price) + (
            risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity) / (
            volatility * math.sqrt(time_to_maturity))


def calculate_d2(d1, volatility, time_to_maturity):
    return d1 - volatility * math.sqrt(time_to_maturity)
