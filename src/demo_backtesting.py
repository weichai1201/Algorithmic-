import os.path
from datetime import datetime

import pandas as pd

from src.backtesting.backtesting import run_daily_market_replay
from src.data_access.data_access import DataAccess
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.rolling_short_put import RollingShortPut
from src.trading_strategies.strategy.strategy_id import StrategyId
import matplotlib.pyplot as plt


# volatility
# (0.010615660972065288, 'KO') (0.010711019177999836, 'JNJ') (0.010799562059302473, 'MCD')
# (0.04465957542892037, 'SMCI') (0.04234928634216114, 'ENPH') (0.04224288734882527, 'EPAM')
start_date = datetime(2005, 1, 1)
end_date = datetime(2022, 1, 1)

def main():
    foldername = "backtesting_result"

    low_vol = ["KO", "JNJ", "MCD"]
    high_vol = []
    high_market_cap = ["MSFT", "AAPL", "NVDA", "GOOG", "AMZN"]
    low_market_cap = ["BEN", "IVZ"]  # https://www.slickcharts.com/sp500
    symbols = low_vol + high_vol + high_market_cap + low_market_cap
    _run(symbols, start_date, end_date, foldername)
    _run(symbols, start_date, end_date, foldername, is_itm=False)
    _run(symbols, start_date, end_date, foldername, is_weekly=False)
    _run(symbols, start_date, end_date, foldername, is_itm=False, is_weekly=False)
    _run(symbols, start_date, end_date, foldername, num_of_strikes=2)


def _run(symbols: [str], start_date, end_date, foldername, is_itm=True, is_weekly=True, num_of_strikes=1,
         weekday="FRI"):
    # output directory
    # option specification
    sub_folder = ""
    if is_itm:
        sub_folder += "itm_"
    else:
        sub_folder += "otm_"
    if is_weekly:
        sub_folder += "weekly_"
    else:
        sub_folder += "monthly_"
    sub_folder += "num-strikes-" + str(num_of_strikes)

    strategies = dict()
    for s in symbols:
        strategy_id = StrategyId("NAKED_PUT_" + s)
        strategy = RollingShortPut(strategy_id, Symbol(s), is_itm, is_weekly, weekday, num_of_strikes)
        strategies[strategy_id] = strategy

    backtester = run_daily_market_replay(strategies, start_date, end_date)

    # write to csv
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    data = backtester.get_data()
    for strategy_id, df in data.items():
        folder_path = os.path.join(foldername, sub_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        filename = os.path.join(folder_path, f"{strategy_id.get_id()}.csv")
        df.to_csv(filename + ".csv")

        df['Cumulative'] = df['Cumulative'].apply(list)
        duplicated_df = pd.DataFrame(
            [[date, cumulative] for date, cumulatives in zip(df['Date'], df['Cumulative']) for cumulative in
             cumulatives], columns=['Date', 'Cumulative'])

        _plot(duplicated_df["Date"], duplicated_df["Cumulative"], strategy_id.get_id(), filename + ".png")
        txt = open(filename + ".txt", "w")
        txt.write(backtester.transactions(strategy_id).__str__())
        txt.close()


def _plot(x, y, title="", filename=""):
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, linestyle="-", label="Naked Put Profit")
    hist_data = DataAccess().get_stock([Symbol(title.split("_")[-1])], start_date, end_date)
    hist_data["Date"] = hist_data["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    plt.plot(hist_data["Date"], hist_data[title.split("_")[-1]], linestyle="-", label="Stock Price")
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


if __name__ == "__main__":
    main()
