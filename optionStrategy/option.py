from datetime import datetime
from optionStrategy.stock_symbol import StockSymbol
from price import Price

class Option:
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price, expiration_date: datetime):
        self.stock_symbol = stock_symbol
        self.strike_price = strike_price
        self.expiration_date = expiration_date

class CallOption(Option):
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price, expiration_date: datetime):
        super().__init__(stock_symbol, strike_price, expiration_date)
        self.option_type = "Call"

class PutOption(Option):
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price, expiration_date: datetime):
        super().__init__(stock_symbol, strike_price, expiration_date)
        self.option_type = "Put"