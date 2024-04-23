strike_gaps = [
    (0, 0.05),
    (2, 0.10),
    (5, 0.25),
    (15, 0.50),
    (50, 1.00),
    (100, 2.00)
]


def get_strike_gap(stock_price: float):
    strike_gap = 0
    for price, gap in strike_gaps:
        if stock_price >= price:
            strike_gap = gap

    return strike_gap


def calculate_strike(stock_price: float, is_itm: bool, num_strikes: int, is_put: bool):
    """
    :param stock_price: current stock price.
    :param is_itm: boolean, if true, itm side; else otm side.
    :param num_strikes: number of strikes offset by stock price.
    :param is_put: put option if true, call option if false.
    :return: Target strike price.

    @author: Yifan Xiao
    """

    strike_gap = get_strike_gap(stock_price)

    if (is_put and is_itm) or (not is_put and not is_itm):
        strike = (int(stock_price / strike_gap) + num_strikes) * strike_gap
    else:
        strike = (int(stock_price / strike_gap) + 1 - num_strikes) * strike_gap

    return strike
