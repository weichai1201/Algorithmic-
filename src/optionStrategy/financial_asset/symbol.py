

class Symbol:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_symbol(self) -> str:
        return self.symbol

    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False
        return self.symbol.__eq__(other.get_symbol())
