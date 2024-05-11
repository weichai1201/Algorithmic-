from src.agent.transactions.positions import Positions
from src.data_access.data_package import DataPackage
from src.market.order import Order
from src.trading_strategies.financial_asset.option import PutOption
from src.trading_strategies.financial_asset.price import Price, EmptyPrice
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.agent.transactions.position import Position
from src.util.expiry_date import next_expiry_date

risk_free_rate = 0.03


class LongPut(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool,
                 is_weekly: bool, weekday, num_of_strikes, scale=1):
        super().__init__(strategy_id, symbol, is_itm, is_weekly,
                         weekday, num_of_strikes, scale)

    def roll_over(self, stock, expiration_date):
        strike_price = calculate_strike(stock.get_price().price(), self._is_itm, self._num_of_strikes, True)
        # premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, True)
        # new_option = PutOption(stock.symbol(), Price(strike_price, stock.get_price().time()), expiration_date, premium)
        return strike_price, expiration_date

    def update(self, new_data: DataPackage) -> Order:
        stock_price = new_data.stock.get_price().price()
        date = new_data.date
        expiry = next_expiry_date(date, self._is_weekly)
        strike_price = self.roll_over(stock_price, expiry)[0]
        next_option = PutOption(self.symbol(), Price(strike_price, date), expiry, EmptyPrice())
        msg = f"Roll over long call. Stock price at {stock_price}."
        order = Order(next_option, date, Positions(Position.LONG, self._scale), msg)
        return order
