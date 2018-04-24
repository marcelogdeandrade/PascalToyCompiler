from value import Value


class SymbolTable():
    def __init__(self):
        self.symbols = {}

    def getSymbol(self, symbol):
        if symbol in self.symbols.keys():
            return self.symbols[symbol]
        else:
            pass

    def setSymbol(self, symbol, value):
        var = self.symbols[symbol]
        var.setValue(value)

    def createSymbol(self, symbol, var_type):
        self.symbols[symbol] = Value(var_type)
