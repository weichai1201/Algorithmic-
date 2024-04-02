from src.trading_strategies.optionStrategy.option_strategy import OptionStrategy


class MarginHandler:
    def __init__(self, strategy: OptionStrategy):
        self.strategy = strategy

    def calculate_margin(self):
        # Calculate margin requirements for each strategy
        pass
