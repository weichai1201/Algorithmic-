import os.path
import timeit
from datetime import datetime
from typing import Callable

import pandas as pd

from src.backtesting.backtesting import run_daily_market_replay
from src.backtesting.stock_selection import StockSelection
from src.data_access.data_access import DataAccess
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.rolling_short_put import RollingShortPut
from src.trading_strategies.strategy.option_strategy.straddle import Straddle
from src.trading_strategies.strategy.strategy_id import StrategyId
import matplotlib.pyplot as plt


# volatility
# (0.010615660972065288, 'KO') (0.010711019177999836, 'JNJ') (0.010799562059302473, 'MCD')
# (0.04465957542892037, 'SMCI') (0.04234928634216114, 'ENPH') (0.04224288734882527, 'EPAM')


def main():
    foldername = "backtesting_result"

    start_date = datetime(2006, 1, 1)
    end_date = datetime(2022, 1, 1)

    symbols = StockSelection().simple
    # beginning of run
    timers = [timeit.default_timer()]
    # default setting
    _run(Straddle, symbols, start_date, end_date, foldername)
    timers.append(timeit.default_timer())
    # out-of-money
    # _run(RollingShortPut, symbols, start_date, end_date, foldername, is_itm=False)
    # timers.append(timeit.default_timer())
    # # monthly expiration
    # _run(RollingShortPut, symbols, start_date, end_date, foldername, is_weekly=False)
    # timers.append(timeit.default_timer())
    # # out-of-money and monthly
    # _run(RollingShortPut, symbols, start_date, end_date, foldername, is_itm=False, is_weekly=False)
    # timers.append(timeit.default_timer())
    # # number of strike gaps is 2
    # _run(RollingShortPut, symbols, start_date, end_date, foldername, num_of_strikes=2)
    # timers.append(timeit.default_timer())

    for i in range(len(timers))[1:]:
        print(f"used time activity {i}: {timers[i] - timers[i - 1]} \n")

    print(f"total time: {timers[len(timers) - 1] - timers[0]} ")


def _run(strategy_func: Callable, symbols: [str], start_date, end_date, foldername, is_itm=True, is_weekly=True, num_of_strikes=1,
         weekday="FRI"):
    # output directory
    # option specification
    sub_folder = ""
    sub_title = ""
    if is_itm:
        sub_folder += "itm_"
        sub_title += "roll in-the-money side, "
    else:
        sub_folder += "otm_"
        sub_title += "roll out-of-money side, "
    if is_weekly:
        sub_folder += "weekly_"
        sub_title += "with weekly expiration, "
    else:
        sub_folder += "monthly_"
        sub_title += "with monthly expiration, "
    sub_folder += "num-strikes-" + str(num_of_strikes)
    sub_title += "number of strikes: " + str(num_of_strikes)

    strategies = dict()
    for s in symbols:
        strategy_id = StrategyId("NAKED_PUT_" + s)
        strategy = strategy_func(strategy_id, Symbol(s), is_itm, is_weekly, weekday, num_of_strikes)
        strategies[strategy_id] = strategy

    backtester = run_daily_market_replay(strategies, start_date, end_date)

    # write to csv
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    if not os.path.exists(f"{foldername}/{sub_folder}"):
        os.makedirs(f"{foldername}/{sub_folder}")

    data = backtester.get_data()
    # output results
    for strategy_id, df in data.items():
        filename = f"{foldername}/{sub_folder}/{strategy_id.get_id()}"

        # profits
        df.to_csv(filename + ".csv")

        # plots
        df['Cumulative'] = df['Cumulative'].apply(list)
        duplicated_df = pd.DataFrame(
            [[date, cumulative] for date, cumulatives in zip(df['Date'], df['Cumulative']) for cumulative in
             cumulatives], columns=['Date', 'Cumulative'])
        symbol = strategies[strategy_id].symbol()
        stock_df = DataAccess().get_stock([symbol], start_date, end_date)
        stock_df["Date"] = stock_df["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        _plot_with_stock(duplicated_df, stock_df, symbol.symbol,
                         title=f"{strategy_id.get_id()}\n{sub_title}", filename=filename + ".png")

        # transaction records
        txt = open(filename + ".txt", "w")
        txt.write(backtester.transactions(strategy_id).__str__())
        txt.close()


def _plot_with_stock(profit_df, stock_df, symbol, title="", filename=""):
    plt.figure(figsize=(14, 8))
    plt.plot(profit_df["Date"], profit_df["Cumulative"], linestyle="-", label="Naked Put Profit")
    plt.plot(stock_df["Date"], stock_df[symbol], linestyle="-", label="Stock Price")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Profit (USD)")
    plt.grid(True)
    plt.legend()
    if filename != "":
        plt.savefig(filename)
    else:
        plt.show()
    plt.clf()
    plt.close()


if __name__ == "__main__":
    main()
