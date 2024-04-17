from src.trading_strategies.strategy.strategy_id import StrategyId


class BacktestingSummary:
    def __init__(self, initial_cash_value=0, end_cash_value=0, profits=dict[StrategyId, float],
                 drawndowns=dict[StrategyId, float],
                 years=1):  # , profits: float[], drawndowns: float[], cagr: float):
        self._initial_cash_value = initial_cash_value
        self._end_cash_value = end_cash_value
        self._profits = profits
        self._drawndowns = drawndowns
        self._cagr = (1 + end_cash_value / initial_cash_value) ** (1 / years) - 1

    def get_profit(self, strategyId: StrategyId):
        return self._profits[strategyId]

    def get_drawndown(self, strategyId: StrategyId):
        return self._drawndowns[strategyId]

    def get_profits(self):
        return self._profits

    def get_drawdowns(self):
        return self._drawndowns

    def get_cagr(self):
        return self._cagr
