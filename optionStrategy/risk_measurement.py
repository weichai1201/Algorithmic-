import datetime
import numpy as np

from optionStrategy.option import Option
from optionStrategy.stock import Stock


"""
Simulate stock price using Geometric Brownian Motion
"""
def simulate_stock_price(stock: Stock, risk_free_rate, time_to_maturity, num_paths, num_steps):
    dt = time_to_maturity / num_steps
    stock_price_paths = np.zeros((num_paths, num_steps + 1))
    stock_price_paths[:, 0] = stock.current_price.price
    for i in range(num_paths):
        for j in range(1, num_steps + 1):
            z = np.random.standard_normal(1)
            stock_price_paths[i, j] = stock_price_paths[i, j - 1] * np.exp(
                (risk_free_rate - 0.5 * stock.volatility ** 2) * dt + stock.volatility * np.sqrt(dt) * z)
    return stock_price_paths

def calculate_var(stock: Stock, option: Option, risk_free_rate, confidence_level, num_paths, num_steps):
    time_to_maturity = (option.expiration_date - stock.current_price.timeStamp) / datetime.timedelta(days=365)
    stock_price_paths = simulate_stock_price(stock, risk_free_rate, time_to_maturity, num_paths, num_steps)
    option_payoff = option.option_payoff(stock_price_paths[:, -1], option.strike_price.price)

    # Calculate option P&L
    option_pl = option_payoff - option.premium
    option_pl_sorted = np.sort(option_pl)

    # Calculate VaR
    var_index = int(num_paths * (1 - confidence_level))
    option_var = -option_pl_sorted[var_index]

    return option_var

def stress_testing():
    # Implement stress testing analysis
    pass

def sensitivity_analysis():
    # Implement sensitivity analysis
    pass