import math
from scipy.stats import norm

class OptionPricer:
    """
    volatility: daily
    risk free rate: continuous
    """
    def __init__(self, stock_price, volatility):
        self.stock_price = stock_price
        self.volatility = volatility

    def calculate_d1(self, strike_price, expiration_date, risk_free_rate):
        return (math.log(self.stock_price / strike_price) + (
                    risk_free_rate + 0.5 * self.volatility ** 2) * expiration_date) / (
                         self.volatility * math.sqrt(expiration_date))

    def estimate_call_price(self, strike_price, expiration_date, risk_free_rate):
        # Implement BSM pricing model for call option
        d1 = self.calculate_d1(strike_price, expiration_date)
        d2 = d1 - self.volatility * math.sqrt(expiration_date)
        call_price = self.stock_price * norm.cdf(d1) - strike_price * math.exp(
            - risk_free_rate * expiration_date) * norm.cdf(d2)
        return call_price

    def estimate_put_price(self, strike_price, expiration_date, risk_free_rate):
        # Implement BSM pricing model for put option
        d1 = self.calculate_d1(strike_price, expiration_date)
        d2 = d1 - self.volatility * math.sqrt(expiration_date)
        put_price = strike_price * math.exp(-risk_free_rate * expiration_date) * norm.cdf(
            -d2) - self.stock_price * norm.cdf(-d1)
        return put_price