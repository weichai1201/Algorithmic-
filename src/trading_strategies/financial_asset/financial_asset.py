from abc import abstractmethod

from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol


class FinancialAsset:
    def __init__(self):
        # TODO: fix financial constructor; define more clearly and simply role of child classes.
        pass

    @abstractmethod
    def symbol(self) -> Symbol:
        pass

    @abstractmethod
    def __str__(self):
        pass

