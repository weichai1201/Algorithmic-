from src.agent.transactions.transactions import Transactions


def calculate_option_payoff(transactions: Transactions) -> tuple[list, list]:
    payoffs = []
    cumulative_payoffs = []
    c = 0
    for transaction in transactions.get_transactions():
        p = transaction.get_payoff()
        payoffs.append(p)
        c += p
        cumulative_payoffs.append(p)
    return payoffs, cumulative_payoffs


def calculate_option_profit(transactions: Transactions) -> tuple[list, list]:
    # at the time of next transaction, previous option is closed
    profits = []
    cumulative_profits = []
    c = 0
    prev_transaction = None
    for transaction in transactions.get_transactions():
        # assume short
        gain = transaction.get_asset().price()
        if prev_transaction is not None:
            gain -= prev_transaction.get_payoff()
        if transaction.is_long():
            gain *= -1
        profits.append(gain)
        c += gain
        cumulative_profits.append(c)
        prev_transaction = transaction
    return profits, cumulative_profits


def calculate_drawdowns(values: [float]) -> (float, [float]):
    percentages = []
    peak = 0
    for value in values:
        peak = max(peak, value)
        if peak == 0:
            percentages.append(0)
        else:
            percentages.append((peak - value) / peak)
    return percentages

