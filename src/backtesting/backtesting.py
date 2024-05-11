from datetime import datetime
from typing import Dict

from src.agent.agent import Agent
from src.backtesting.daily_market_replay import DailyMarketReplay
from src.trading_strategies.strategy.strategy import Strategy
from src.trading_strategies.strategy.strategy_id import StrategyId


def run_daily_market_replay(strategies: Dict[StrategyId, Strategy], start_date: datetime, end_date: datetime):
    agent = Agent(strategies)
    backtester = DailyMarketReplay(start_date, end_date, agent, [])
    backtester.run_back_testing()
    return backtester


def run_multi_agent():
    pass
