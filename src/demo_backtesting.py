import os.path
from datetime import datetime

from src.backtesting.backtesting import run_daily_market_replay
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.rolling_short_put import RollingShortPut
from src.trading_strategies.strategy.strategy_id import StrategyId
import matplotlib.pyplot as plt


# (0.010615660972065292, 'KO')(0.010711019177999836, 'JNJ')(0.010799562059302475, 'MCD')

def main():
    # output directory
    foldername = "backtesting_result"

    start_date = datetime(2009, 1, 1)
    end_date = datetime(2010, 1, 1)
    symbol_strs = ["SMCI", "KO", "AAPL", "CMA", "RHI"]
    symbol_low_vol = ["KO", "JNJ", "MCD"]

    # option specification
    is_itm = True
    is_weekly = False
    weekday = "FRI"
    num_strike = 1

    strategies = dict()
    for s in ["AAPL"]:
        strategy_id = StrategyId("NAKED_PUT_" + s)
        strategy = RollingShortPut(strategy_id, Symbol(s), is_itm, is_weekly, weekday, num_strike)
        strategies[strategy_id] = strategy

    backtester = run_daily_market_replay(strategies, start_date, end_date)



# write to csv
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    data = backtester.get_data()
    for strategy_id, df in data.items():
        filename = f"{foldername}/{strategy_id.get_id()}"
        df.to_csv(filename + ".csv")
        _plot(df["Date"], df["Cumulative"], strategy_id.get_id(), filename + ".png")
        txt = open(filename + ".txt", "w")
        txt.write(backtester.transactions(strategy_id).__str__())
        txt.close()


def _plot(x, y, title="", filename=""):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linestyle="-")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Profit (USD)")
    plt.grid(True)
    if filename != "":
        plt.savefig(filename)
    else:
        plt.show()


if __name__ == "__main__":
    main()
