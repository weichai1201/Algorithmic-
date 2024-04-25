from datetime import timedelta, datetime

from src.backtesting.agent import Agent
from src.backtesting.backtester import Backtester, DailyMarketReplay
from src.trading_strategies.financial_asset.symbol import Symbol
from src.trading_strategies.strategy.option_strategy.naked_put import NakedPut
from src.trading_strategies.strategy.strategy_id import StrategyId


def main():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    strategy_id = StrategyId("NAKED_PUT_AAPL")
    naked_put = NakedPut(strategy_id, Symbol("AAPL"), None, False)
    agent = Agent({strategy_id: naked_put})
    backtester = DailyMarketReplay(start_date, end_date, agent,[])
    backtester.run_back_testing()
    print(backtester.transactions())


if __name__ == "__main__":
    main()
