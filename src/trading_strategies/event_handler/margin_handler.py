from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy


class MarginHandler:
    def __init__(self, margin_para1: float, margin_para2: float):
        self.margin_para1 = margin_para1
        self.margin_para2 = margin_para2

    def calculate_margin(self):
        # Calculate margin requirements for each strategy
        pass

    def _margin1(self, underlying_value, otm_amount, premium):
        return self.margin_para1 * underlying_value - otm_amount + premium

    def _margin2(self, contract_value, premium):
        return self.margin_para2 * (contract_value + premium)

    def naked_call_margin(self, underlying_value, strike_price, premium):
        otm_amount = max(0, strike_price - underlying_value)
        margin1 = self._margin1(underlying_value, otm_amount, premium)
        margin2 = self._margin2(underlying_value, premium)
        margin3 = 1
        return max(margin1, margin2, margin3)

    def naked_put_margin(self, underlying_value, strike_price, premium):
        otm_amount = max(0, underlying_value - strike_price)
        margin1 = self._margin1(underlying_value, otm_amount, premium)
        margin2 = self._margin2(strike_price, premium)
        margin3 = 1
        return max(margin1, margin2, margin3)

    def straddle_margin(self, call_underlying_value, call_strike_price, call_premium, put_underlying_value,
                              put_strike_price, put_premium):
        naked_call_margin = self.naked_call_margin(call_underlying_value, call_strike_price, call_premium)
        naked_put_margin = self.naked_put_margin(put_underlying_value, put_strike_price, put_premium)
        if naked_call_margin > naked_put_margin:
            return naked_call_margin + put_premium
        else:
            return naked_put_margin + call_premium

    def spread_margin(self, strike_long, strike_short):
        return abs(strike_long - strike_short)


class EquityMarginHandler(MarginHandler):
    def __init__(selfy):
        super().__init__(margin_para1=0.2, margin_para2=0.1)


class IndexMarginHandler(MarginHandler):
    def __init__(self):
        super().__init__(margin_para1=0.15, margin_para2=0.1)


