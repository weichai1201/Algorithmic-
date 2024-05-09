from datetime import datetime

from src.agent.agent import Agent
from src.backtesting.daily_market_replay import DailyMarketReplay
from src.trading_strategies.strategy.strategy import Strategy


def run_daily_market_replay(strategies: list[Strategy], start_date: datetime, end_date: datetime):
    strategies_dict = dict()
    for s in strategies:
        strategies_dict[s.id()] = s
    agent = Agent(strategies_dict)
    backtester = DailyMarketReplay(start_date, end_date, agent, [])
    backtester.run_back_testing()


def run_multi_agent():
    pass
