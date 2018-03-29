class SymbolTable():
    def __init__(self):
        self.symbols = {}

    def getSymbol(self, symbol):
        if symbol in self.symbols.keys():
            return self.symbols[symbol]
        else:
            pass

    def setSymbol(self, symbol, value):
        self.symbols[symbol] = value
