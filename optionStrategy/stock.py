from datetime import datetime
from optionStrategy.price import Price
from optionStrategy.stock_symbol import StockSymbol

class Stock:
    def __init__(self, stock_symbol: StockSymbol, price: [Price]):
        self.stock_symbol = stock_symbol
        self.price = price
