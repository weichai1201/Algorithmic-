from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from src.trading_strategies.financial_asset.option import PutOption
from src.trading_strategies.financial_asset.price import Price
from src.trading_strategies.financial_asset.stock import Stock
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.option_pricing import bsm_pricing, implied_t_put
from src.trading_strategies.strategy.option_strategy.naked_put import NakedPut
from src.trading_strategies.strategy.option_strategy.option_strike import calculate_strike
from src.trading_strategies.strategy.strategy_id import StrategyId
from src.util.expiry_date import next_expiry_date
from src.util.read_file import read_file, get_historical_values
import pandas as pd


def main():
    csl_symbol = Symbol("CSL.AX")

    file_path = '/Users/yifanxiao/Desktop/csl.csv'
    stock_data = get_historical_values(csl_symbol, file_path, '2004-01-01', '2024-03-31')
    stock_data.set_index('Date', inplace=True)
    # print(stock_data.loc['2004-03-31'].iloc[-1])

    date = datetime(2004, 3, 31)
    price = Price(stock_data.loc[date.strftime('%Y-%m-%d')].iloc[-1], date)
    csl_stock = Stock(csl_symbol, price)

    # print(csl_stock.garch_long_run)

    date = next_expiry_date(date, "thu", False, False)

    strike_price = Price(calculate_strike(csl_stock.current_price.price(), False, 1, True), date)

    # dividend = Price(0.5, datetime(2004, 4, 11))
    # dividends = [dividend]

    premium = bsm_pricing(csl_stock, strike_price.price(), date, [], 0.03, False)
    put_option = PutOption(csl_symbol, strike_price, date, premium)

    # marginHandler = EquityMarginHandler()
    # margin = marginHandler.naked_put_margin(csl_stock.current_price.price(), put_option.get_strike().price(),
    #                                         put_option.get_premium().price())
    # # print(margin)
    #
    # imply_t = 365 * implied_t_put(csl_stock.current_price.price(), 5.25, 0.03, 0.3, csl_stock.garch_long_run)
    # print(imply_t)

    profit = []

    for i in range(44):
        naked_put = NakedPut(StrategyId("1"), [put_option], False, False)

        transaction = naked_put.roll(put_option, csl_stock.current_price.time())
        profit.append((transaction.calculate_premium(), transaction.get_time()))

        date = put_option.get_expiry()
        csl_stock.set_current_price(Price(stock_data.loc[date.strftime('%Y-%m-%d')].iloc[-1], date))

        put_option = naked_put.update(csl_stock)

        profit.append((-transaction.calculate_payoff(csl_stock.current_price), csl_stock.current_price.time()))



    sum = []

    total = 0
    for data in profit:
        total += data[0]
        sum.append((total, data[1]))

    print(sum)

    x = [d[1].strftime('%Y-%m-%d') for d in sum]  # Convert datetime to string
    y = [d[0] for d in sum]

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title('Plot of Data')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    pass

if __name__ == "__main__":
    main()