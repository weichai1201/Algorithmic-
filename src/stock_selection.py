# 2 x stock with high historical volatility (>50%)  SMCI, ENPH
# 2 x stock with low historical volatility (<25%)  KO, JNJ
# 1 x stock with low or possibly negative beta (say beta < 0.2).
# 1 x stock which has paid a dividend every year for at least 10 years
# 2 x large cap stock (market cap >$10b)  AAPL, MSFT
# 2 x small cap stock (market cap <$500m)  CMA, MHK
import statistics

import numpy as np

from src.util.read_file import read_file


def main():
    stock_filename = "data/sp500_adj_close_prices.csv"
    data = read_file(stock_filename)
    result = []
    for symbol in data.columns[1:]:
        try:
            tmp = data[symbol]
            prices = data[symbol].tail(min(500, len(tmp))).tolist()
            returns = np.diff(prices) / prices[:-1]
            result.append((statistics.stdev(returns), symbol))
        except AttributeError:
            pass
    result = sorted(result)
    print(result[0], result[1])
    print(result[len(result) - 1], result[len(result) - 2])


if __name__ == "__main__":
    main()
