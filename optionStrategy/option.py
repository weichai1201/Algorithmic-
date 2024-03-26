from datetime import datetime
from optionStrategy.stock_symbol import StockSymbol
from price import Price

class Option:
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price):
        self.stock_symbol = stock_symbol
        self.strike_price = strike_price

class CallOption(Option):
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price):
        super().__init__(stock_symbol, strike_price)
        self.option_type = "Call"

class PutOption(Option):
    def __init__(self, stock_symbol: StockSymbol, strike_price: Price):
        super().__init__(stock_symbol, strike_price)
        self.option_type = "Put"