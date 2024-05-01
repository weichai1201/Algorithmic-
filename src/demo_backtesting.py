import os.path
from datetime import datetime

from src.agent.agent import Agent
from src.backtesting.backtester import DailyMarketReplay
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.naked_put import NakedPut
from src.trading_strategies.strategy.strategy_id import StrategyId
import matplotlib.pyplot as plt


def main():
    start_date = datetime(2004, 1, 1)
    end_date = datetime(2010, 1, 1)

    foldername = "tmp"
    symbol_strs = ["SMCI", "KO", "AAPL", "CMA", "RHI"]
    # volatility
    # (0.010615660972065292, 'KO')(0.010711019177999836, 'JNJ')(0.010799562059302475, 'MCD')
    symbol_low_vol = ["KO", "JNJ", "MCD"]
    strategies = dict()
    for s in ["KO"]:
        strategy_id = StrategyId("NAKED_PUT_" + s)
        strategy = NakedPut(strategy_id, Symbol(s), None, False)
        strategies[strategy_id] = strategy
    agent = Agent(strategies)
    backtester = DailyMarketReplay(start_date, end_date, agent, [])
    backtester.run_back_testing()

    # demo print
    # try:
    #     print(backtester.transactions(StrategyId("NAKED_PUT_SMCI")))
    # except KeyError:
    #     pass

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
