from datetime import datetime

import numpy as np
from arch import arch_model

from src.data_access.data_access import DataAccess
from src.data_access.volatility import VolatilityType, Volatility
from src.trading_strategies.financial_asset.symbol import Symbol


def calculate_vol(volatility_type: VolatilityType, symbol: Symbol, start: datetime, end: datetime) -> Volatility:
    if volatility_type == VolatilityType.GARCH:
        value = calculate_garch(symbol, start, end)
    else:
        value = 0
    return Volatility(value, volatility_type)


def get_returns(symbol: Symbol, start_date: datetime, end_date: datetime):
    # TODO: timeframe might not in the data_access
    da = DataAccess()
    data = da.get_stock([symbol], start_date, end_date)
    prices = [p for p in data[[symbol]] if not np.isnan(p)]
    return np.diff(prices) / prices[:-1]


def calculate_garch(symbol: Symbol, start_date, end_date):
    returns = get_returns(symbol, start_date, end_date)
    model = arch_model(returns, vol='GARCH', p=1, q=1, rescale=False)
    fit = model.fit(disp='off')
    vol = np.sqrt(fit.forecast(horizon=100).variance).mean(axis=1).iloc[-1]
    return vol * np.sqrt(252)
