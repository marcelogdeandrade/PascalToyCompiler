class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def Evaluate(self):
        pass


class BinOp(Node):
    def Evaluate(self):
        value1 = self.children[0].Evaluate()
        value2 = self.children[1].Evaluate()
        if (self.value == "+"):
            return value1 + value2
        elif (self.value == "-"):
            return value1 - value2
        elif (self.value == "*"):
            return value1 * value2
        elif (self.value == "/"):
            return value1 // value2
        else:
            #tratar erro
            return

class UnOp(Node):
    def Evaluate(self):
        value = self.children[0].Evaluate()
        if (self.value == "-"):
            return value * -1
        else:
            #tratar erro
            return

class IntVal(Node):
    def Evaluate(self):
        return int(self.value)

class NoOp(Node):
    def Evaluate(self):
        return None