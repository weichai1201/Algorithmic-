import os.path
import timeit
from datetime import datetime
from typing import Callable

import pandas as pd

from src.backtesting.backtesting import run_daily_market_replay
from src.backtesting.backtesting_config import OptionBacktestConfigBundle, OptionBacktestConfig
from src.backtesting.stock_selection import StockSelection
from src.data_access.data_access import DataAccess
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.long_call import LongCall
from src.trading_strategies.strategy.option_strategy.long_put import LongPut
from src.trading_strategies.strategy.option_strategy.short_call import ShortCall
from src.trading_strategies.strategy.option_strategy.short_put import ShortPut
from src.trading_strategies.strategy.option_strategy.straddle import Straddle
from src.trading_strategies.strategy.option_strategy.strangle import Strangle
from src.trading_strategies.strategy.strategy_id import StrategyId
import matplotlib.pyplot as plt


# volatility
# (0.010615660972065288, 'KO') (0.010711019177999836, 'JNJ') (0.010799562059302473, 'MCD')
# (0.04465957542892037, 'SMCI') (0.04234928634216114, 'ENPH') (0.04224288734882527, 'EPAM')


def main():
    foldername = "backtesting_result"

    symbols = StockSelection().simple
    # long_call_configs = OptionBacktestConfigBundle(LongCall)
    # long_put_configs = OptionBacktestConfigBundle(LongPut)
    short_call_configs = OptionBacktestConfigBundle(ShortCall)
    short_put_configs = OptionBacktestConfigBundle(ShortPut)
    straddle_configs = OptionBacktestConfigBundle(Straddle)
    # strangle_configs = OptionBacktestConfigBundle(Strangle)
    configs = short_call_configs.configs + short_put_configs.configs + straddle_configs.configs
    # beginning of run
    timers = [timeit.default_timer()]

    for config in configs:
        _run_config(config, symbols, foldername)
        timers.append(timeit.default_timer())
        t_diff = timers[len(timers) - 1] - timers[len(timers) - 2]
        print(f"Finished running backtesing in {round(t_diff, 2)} seconds"
              f" for {len(symbols)} companies with:"
              f"\n{config}\n")
    #


def _run_config(config: OptionBacktestConfig, symbols, foldername):
    _run_option(strategy_func=config.strategy, symbols=symbols, foldername=foldername,
                start_date=config.start_date, end_date=config.end_date,
                is_itm=config.is_itm, is_weekly=config.is_weekly,
                num_of_strikes=config.num_of_strikes, weekday=config.weekday,
                max_strike=config.max_strike)


def _run_option(strategy_func: Callable, symbols: [str], foldername, start_date, end_date, is_itm=True, is_weekly=True,
                num_of_strikes=1,
                weekday="FRI",
                max_strike=True):
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
    if not max_strike:
        sub_folder += "minStrike_"
        sub_title += "resolve strikes with MIN, "
    sub_folder += "num-strikes-" + str(num_of_strikes)
    sub_title += "number of strikes: " + str(num_of_strikes)

    strategies = dict()
    for s in symbols:
        strategy_id = StrategyId(f"{strategy_func.__name__}-{s}")
        strategy = strategy_func(strategy_id, Symbol(s), is_itm, is_weekly, weekday, num_of_strikes, 1, max_strike)
        strategies[strategy_id] = strategy

    backtester = run_daily_market_replay(strategies, start_date, end_date)

    # write to csv
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    # if not os.path.exists(f"{foldername}/{sub_folder}"):
    #     os.makedirs(f"{foldername}/{sub_folder}")

    data = backtester.get_data()
    # output results
    for strategy_id, df in data.items():
        filename = f"{foldername}/{strategy_id.get_id()}_{sub_folder}"

        # profits
        df.to_csv(filename + ".csv")

        # plots
        # df['Cumulative'] = df['Cumulative'].apply(list)
        # duplicated_df = pd.DataFrame(
        #     [[date, cumulative] for date, cumulatives in zip(df['Date'], df['Cumulative']) for cumulative in
        #      cumulatives], columns=['Date', 'Cumulative'])
        symbol = strategies[strategy_id].symbol()
        stock_df = DataAccess().get_stock([symbol], start_date, end_date)
        stock_df["Date"] = stock_df["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        _plot_with_stock(df, stock_df, symbol.symbol,
                         title=f"{strategy_id.get_id()}\n{sub_title}",
                         filename=filename + ".png",
                         strategy_name=strategy_id.get_id())

        # transaction records
        txt = open(filename + ".txt", "w")
        txt.write(backtester.transactions(strategy_id).__str__())
        txt.close()


def _plot_with_stock(profit_df, stock_df, symbol, title="", filename="", strategy_name=""):
    plt.figure(figsize=(14, 8))
    plt.plot(profit_df["Date"], profit_df["Cumulative"], linestyle="-", label=strategy_name)
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
