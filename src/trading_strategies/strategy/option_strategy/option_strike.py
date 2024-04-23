strike_gaps = [
    (0, 0.05),
    (2, 0.10),
    (5, 0.25),
    (15, 0.50),
    (50, 1.00),
    (100, 2.00)
]


def get_strike_gap(stock_price):
    strike_gap = 0
    for price, gap in strike_gaps:
        if stock_price >= price:
            strike_gap = gap

    return strike_gap


def calculate_strike(stock_price, itm_otm, num_strikes, put_call):
    strike_gap = get_strike_gap(stock_price)

    if (put_call and itm_otm) or (not put_call and not itm_otm):
        strike = (int(stock_price / strike_gap) + num_strikes) * strike_gap
    else:
        strike = (int(stock_price / strike_gap) + 1 - num_strikes) * strike_gap

    return strike
