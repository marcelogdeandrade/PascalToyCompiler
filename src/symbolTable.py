from value import Value


class SymbolTable():
    def __init__(self, parent):
        self.symbols = {}
        self.parent = parent

    def getSymbol(self, symbol, symbol_type=None):
            if symbol in self.symbols.keys():
                value = self.symbols[symbol]
                if symbol_type is not None and symbol_type != value.getType():
                    value = self.parent.getSymbol(symbol, symbol_type)
                    return value
                else:
                    return value
            else:
                if self.parent is not None:
                    symbol = self.parent.getSymbol(symbol)
                    return symbol
                else:
                    raise ValueError("Variable {} not declared \
                                         ".format(symbol))

    def setSymbol(self, symbol, value):
        if symbol in self.symbols.keys():
            var = self.symbols[symbol]
            var.setValue(value)
        else:
            if self.parent is not None:
                self.parent.setSymbol(symbol, value)
            else:
                raise ValueError("Variable {} not declared \
                                         ".format(symbol))

    def createSymbol(self, symbol, var_type):
        self.symbols[symbol] = Value(var_type)
