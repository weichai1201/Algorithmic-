from src.trading_strategies.financial_asset.option import PutOption, Option
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing, implied_date
from src.trading_strategies.strategy.option_strategy.option_strategy import OptionStrategy
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike, roll_down_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.trading_strategies.transactions.position import Position
from src.util.expiry_date import closest_expiration_date, nyse_calendar

risk_free_rate = 0.03

class NakedPut(OptionStrategy):

    def __init__(self, strategy_id: StrategyId, symbol: Symbol, is_itm: bool, position: Position,
                 is_weekly: bool, weekday="THU", num_of_strikes=1, scale=1):
        super().__init__(strategy_id, symbol, is_itm, position, is_weekly,
                         weekday, num_of_strikes, scale)

    def _roll_over_put(self, stock, expiration_date):
        strike_price = calculate_strike(stock.current_price.price(), self._is_itm, self._num_of_strikes, True)
        premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, True)
        new_option = PutOption(stock.symbol, Price(strike_price, stock.current_price.time()), expiration_date, premium)
        return new_option

    def _roll_down(self, stock, option, premium) -> Option:
        strike_price = roll_down_strike(stock.current_price.price(), option.get_strike().price(), self._num_of_strikes)
        new_expiration = implied_date(stock.current_price, strike_price, risk_free_rate, premium,
                                      stock.calculate_garch(), True)
        new_expiration = closest_expiration_date(new_expiration, nyse_calendar)
        premium = bsm_pricing(stock, strike_price, new_expiration, [], risk_free_rate, True)
        strike = Price(strike_price, stock.current_price.time())
        new_option = PutOption(stock.symbol, strike, new_expiration, premium)
        return new_option

    # def in_the_money(self, stock_price: float, option) -> bool:
    #     return option.in_the_money(stock_price)
    #
    # def itm_amount(self, stock_price: float, option) -> float:
    #     return option.itm_amount(stock_price)

    # def roll_over(self):
    #     """
    #     Initialisation and expiry with OTM.
    #     :param price: stock price.
    #     :param itm_or_otm: set the strike price relatively greater or less than stock price.
    #     :param premium: the price of the option
    #     :return: `Transaction` order to `Agent`.
    #
    #     @author: Huanjie Zhang
    #     """
    #
    #     current_option = self._options[0]
    #     positions = Positions(Position.SHORT, self._scale)
    #
    #     return Transaction(positions, current_option, current_option.get_expiry())  # timezone maybe a problem
    #
    # def roll_down(self):
    #     """
    #     When the option is itm, roll down the next strike price based on current one
    #     :param num_strikes:
    #     :param premium:
    #     :param stock_price:
    #     :param implied_time:
    #     :return: `Transaction` order to `Agent`.
    #
    #     @author: Huanjie Zhang
    #     """
    #
    #     # request the following
    #     current_option = self._options[0]
    #     positions = Positions(Position.SHORT, self._scale)
    #
    #     return Transaction(positions, current_option, current_option.get_expiry())
    #
    # def roll_up(self):
    #     return
    #
    # def roll(self, new_option, current_time) -> Optional[Transaction]:
    #     positions = Positions(Position.SHORT, self._scale)
    #     return Transaction(positions, new_option, current_time)
    #
    # def update(self, new_stock: Stock, option) -> Optional[Option]:
    #     stock = new_stock
    #     current_time = stock.current_price.time()
    #     stock_price = stock.current_price.price()
    #
    #     if not option.is_expired(current_time):
    #         return None
    #
    #     if option.in_the_money(stock_price):
    #         return self._update_itm_option(stock, current_time, option)
    #     else:
    #         return self._update_otm_option(stock, current_time)
    #
    # def _update_itm_option(self, stock: Stock, option: Option) -> Option:
    #     stock_price = stock.current_price.price()
    #     premium = option.itm_amount(stock_price) + get_strike_gap(stock_price)
    #     strike_price = roll_down_strike(stock_price, option.get_strike().price(), self._num_of_strikes)
    #     new_expiration = implied_date(stock.current_price, strike_price, risk_free_rate, premium, stock.calculate_garch(), True)
    #     new_expiration = closest_expiration_date(new_expiration, asx_calendar)
    #     strike = Price(strike_price, new_expiration)
    #     new_option = PutOption(stock.symbol, strike, new_expiration, premium)
    #     return new_option
    #
    # def _update_otm_option(self, stock: Stock) -> Option:
    #     self._consecutive_itm = 0
    #     expiration_date = next_expiry_date(stock.current_price.time(), self._weekday, self._is_weekly)
    #     strike_price = calculate_strike(stock.current_price.price(), self._is_itm, self._num_of_strikes, True)
    #     premium = bsm_pricing(stock, strike_price, expiration_date, [], risk_free_rate, False)
    #     new_option = PutOption(stock.symbol, Price(strike_price, stock.current_price.time()), expiration_date, premium)
    #     return new_option




