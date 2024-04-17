from src.trading_strategies.option_strategy.option_strategy import OptionStrategy


class MarginHandler:
    def __init__(self, strategy: OptionStrategy):
        self.strategy = strategy

    def calculate_margin(self):
        # Calculate margin requirements for each strategy
        pass

    """
    Equity Options (per contract margin)
    """
    def naked_call_margin(self, underlying_value, strike_price, premium):
        otm_amount = max(0, strike_price - underlying_value)
        margin1 = 0.2 * underlying_value - otm_amount + premium
        margin2 = 0.1 * underlying_value + premium
        margin3 = 1
        return max(margin1, margin2, margin3) * 100

    def naked_put_margin(self, underlying_value, strike_price, premium):
        otm_amount = max(0, underlying_value - strike_price)
        margin1 = 0.2 * underlying_value - otm_amount + premium
        margin2 = 0.1 * strike_price + premium
        margin3 = 1
        return max(margin1, margin2, margin3) * 100

    def straddle_margin(self, call_underlying_value, call_strike_price, call_premium, put_underlying_value,
                              put_strike_price, put_premium):
        naked_call_margin = self.naked_call_margin(call_underlying_value, call_strike_price, call_premium)
        naked_put_margin = self.naked_put_margin(put_underlying_value, put_strike_price, put_premium)
        return max(naked_call_margin, naked_put_margin) + put_premium if (naked_call_margin > naked_put_margin) else call_premium

    def spread_margin(self, strike_long, strike_short):
        return abs(strike_long - strike_short) * 100

