from datetime import datetime

from src.trading_strategies.financial_asset.financial_asset import FinancialAsset
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol


class DataAccessResult:
    def __init__(self, is_successful: bool, data: FinancialAsset):
        self.is_successful = is_successful
        self.data = data


def request_historical_price(symbol: Symbol, date: datetime) -> DataAccessResult:
    pass
