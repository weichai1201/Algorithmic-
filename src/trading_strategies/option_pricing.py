import datetime

import numpy as np
from scipy.stats import norm
import math
from scipy.optimize import newton, minimize

from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
import src.util.util as util
from src.util.expiry_date import next_nth_trading_day

"""
@:param volatility: annual
@:param risk free rate: continuous
"""


def bsm_pricing(stock: Stock, strike: float, expiration_date, dividends: list[Price], risk_free_rate, is_call):
    time_to_maturity = (expiration_date - stock.current_price.time()) / datetime.timedelta(days=365)
    volatility = stock.garch()
    adjusted_price = adjust_dividends(stock, dividends, risk_free_rate)
    if is_call:
        return calculate_call_price(adjusted_price, strike, volatility, time_to_maturity, risk_free_rate)
    else:
        return calculate_put_price(adjusted_price, strike, volatility, time_to_maturity, risk_free_rate)


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
            volatility * np.sqrt(time_to_maturity))


def calculate_d2(d1, volatility, time_to_maturity):
    return d1 - volatility * np.sqrt(time_to_maturity)


def adjust_dividends(stock, dividends, risk_free):
    stock_price = stock.current_price.price()
    for dividend in dividends:
        stock_price -= dividend.price() * math.exp(
            (stock.current_price.time() - dividend.time()) / datetime.timedelta(days=365) * risk_free)

    return stock_price


def implied_t_put(stock_price, strike_price, risk_free_rate, premium, volatility, default_time: float = 60 / 365):
    error_function = lambda t: calculate_put_price(stock_price, strike_price, volatility, t, risk_free_rate) - premium
    try:
        implied_t = newton(error_function, x0=0.15, maxiter=1000)
        return implied_t
    except RuntimeError:
        print(f"Fail to converge with stock: {stock_price}, strike: {strike_price},"
              f" rf: {risk_free_rate}, premium: {premium}, volatility: {volatility}")
        return default_time


def implied_t_call(stock_price, strike_price, risk_free_rate, premium, volatility):
    error_function = lambda t: calculate_call_price(stock_price, strike_price, volatility, t, risk_free_rate) - premium
    implied_t = newton(error_function, x0=0.15)
    return implied_t


def implied_date(stock_price: Price, strike_price, risk_free_rate, premium, volatility, is_put):
    if is_put:
        error_function = lambda t: abs(calculate_put_price(stock_price.price(), strike_price, volatility, t, risk_free_rate) - premium)
    else:
        error_function = lambda t: abs(calculate_call_price(stock_price.price(), strike_price, volatility, t, risk_free_rate) - premium)
    result = minimize(error_function, x0=0.1, bounds=[(0.02, 2)], method='Nelder-Mead')
    implied_t = result.x[0]
    return next_nth_trading_day(stock_price.time(), int(implied_t*252))