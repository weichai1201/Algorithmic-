from datetime import datetime
from optionStrategy.price import Price
from optionStrategy.stock_symbol import StockSymbol

class StockPrice:
    def __init__(self, stock_symbol: StockSymbol, timestamp: datetime, price: Price):
        self.stock_symbol = stock_symbol
        self.timestamp = timestamp
        self.price = price
