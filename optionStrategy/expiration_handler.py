from optionStrategy.option_strategy import OptionStrategy
from optionStrategy.price import Price


class ExpirationHandler:
    def __init__(self, strategy: OptionStrategy, stock_price: Price):
        self.strategy = strategy
        self.stock_price = stock_price

    def assess_option(self):
        # Determine if option is ITM, OTM, or deep OTM at expiry
        pass

    def adjust_option(self):
        # Implement rules for expiration management based on user-defined settings
        pass
