import datetime
import matplotlib.pyplot as plt

from src.trading_strategies.financial_asset.option import PutOption, CallOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing
from src.trading_strategies.strategy.option_strategy.naked_call import NakedCall
from src.trading_strategies.strategy.option_strategy.naked_put import NakedPut
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.agent.transactions.position import Position
from src.util.expiry_date import next_expiry_date, closest_expiration_date
from src.util.read_file import get_historical_values
import pandas as pd


def main():
    file_path = '../src/data/sp500_adj_close_prices.csv'
    symbol = Symbol('RHI')
    date = datetime.datetime(2008, 1, 4, 0, 0)
    end_date = datetime.datetime(2010, 1, 4, 0, 0)
    is_itm = True
    num_strike = 1
    is_weekly = False
    weekday = "FRI"
    is_put = False

    stock_data = get_historical_values(symbol, file_path, date.strftime('%Y-%m-%d'))
    stock_data.set_index('Date', inplace=True)

    price: float = stock_data.loc[date.strftime('%Y-%m-%d %H:%M:%S')].iloc[-1]
    stock: Stock = Stock(symbol, Price(price, date))

    expiry_date = next_expiry_date(date, is_weekly, True)
    strike_price = Price(calculate_strike(price, is_itm, num_strike, is_put), stock.get_price().time())
    premium = bsm_pricing(stock, strike_price.price(), expiry_date, [], 0.03, is_put)

    profit = []

    if is_put:
        put_option = PutOption(symbol, strike_price, expiry_date, premium)
        naked_put = NakedPut(StrategyId("1"), symbol, is_itm, Position.SHORT, is_weekly, weekday, num_strike)

        transaction = naked_put.update(price, put_option, date)

        while date < end_date:
            if naked_put.update(price, put_option, date) is not None:
                if put_option.get_expiry() == date:
                    profit.append((-transaction.calculate_payoff(stock.get_price()), date))
                    transaction = naked_put.update(price, put_option, date)
                    put_option = transaction.get_asset()
                    continue
                else:
                    profit.append((transaction.calculate_premium(), date))

            date = closest_expiration_date(stock.get_price().time() + datetime.timedelta(days=1))
            stock.update_price(Price(stock_data.loc[date.strftime('%Y-%m-%d %H:%M:%S')].iloc[-1], date))

    else:
        call_option = CallOption(symbol, strike_price, expiry_date, premium)
        naked_call = NakedCall(StrategyId("1"), symbol, is_itm, Position.SHORT, is_weekly, weekday, num_strike)

        transaction = naked_call.update(price, call_option, date)

        while date < end_date:
            if naked_call.update(price, call_option, date) is not None:
                if call_option.get_expiry() == date:
                    profit.append((-transaction.calculate_payoff(stock.get_price()), date))
                    transaction = naked_call.update(price, call_option, date)
                    call_option = transaction.get_asset()
                    continue
                else:
                    profit.append((transaction.calculate_premium(), date))

            date = closest_expiration_date(stock.get_price().time() + datetime.timedelta(days=1))
            stock.update_price(Price(stock_data.loc[date.strftime('%Y-%m-%d %H:%M:%S')].iloc[-1], date))

    profit_sum = []

    total = 0
    for data in profit:
        total += data[0]
        # print(data[1], data[0])
        profit_sum.append((data[1], total))

    df_sum = pd.DataFrame(profit_sum, columns=['Date', 'Profit'])
    prices = stock_data.loc[:date.strftime('%Y-%m-%d %H:%M:%S')]

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df_sum['Date'], df_sum['Profit'], linestyle='-')
    plt.plot(prices.index, prices[symbol.symbol], linestyle='-')
    plt.title(f'{symbol.symbol} Stock price & {"Naked Put" if is_put else "Naked Call"} Profit over Time '
              f'({"ITM" if is_itm else "OTM"} by {num_strike} strike)')
    plt.xlabel('Date')
    plt.ylabel('US Dollar')
    plt.grid(True)
    plt.show()

    pass


if __name__ == "__main__":
    main()

    # marginHandler = EquityMarginHandler()
    # margin = marginHandler.naked_put_margin(csl_stock.current_price.price(), put_option.get_strike().price(),
    #                                         put_option.get_premium().price())
    # # print(margin)
    #
    # imply_t = 365 * implied_t_put(csl_stock.current_price.price(), 5.25, 0.03, 0.3, csl_stock.garch_long_run)
    # print(imply_t)
