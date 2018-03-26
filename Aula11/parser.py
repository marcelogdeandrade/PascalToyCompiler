from tokenizer import Tokenizer
from node import BinOp, UnOp, IntVal, NoOp, Print, Identifier, Statements, StrVal

class Parser():
    def __init__(self, origin):
        self.tokens = Tokenizer(origin)
        self.tokens.selectNext()
    def parseStatements(self):
        token = self.tokens.actual
        if token.type == "begin":
            result = Statements(None, [])
            while True:
                result.children.append(self.parseStatement())
                token = self.tokens.actual
                if (token.type == "SEMI_COLON"):
                    pass
                elif (token.type == "end"):
                    break
                else:
                    raise ValueError("Invalid token, expecting a semi colon or a end on position {}".format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a begin on position {}".format(self.tokens.position))
        return result
    def parseStatement(self):
        token = self.tokens.selectNext()
        if token.type == "begin":
            result = self.parseStatements()
        elif token.type == "IDE":
            result = self.parseAtribution()
        elif token.type == "print":
            result = self.parsePrint()
        else:
            raise ValueError("Invalid token, expecting a begin or identifier or print on position {}".format(self.tokens.position))
        return result
    def parseAtribution(self):
        value1 = StrVal(self.tokens.actual.value, [])
        token = self.tokens.selectNext()
        if (token.type == "ATRIBUTE"):
            value2 = self.parseExpression()
            result = BinOp(":=", [value1, value2])
        else:
            raise ValueError("Invalid token, expecting a := on position {}".format(self.tokens.position))  
        return result  
    def parsePrint(self):
        token = self.tokens.selectNext()
        if token.type == "OPEN_PAR":
            value = self.parseExpression()
            token = self.tokens.actual
            if token.type == "CLOSE_PAR":
                result = Print(value, [value])
                self.tokens.selectNext()
            else:
                raise ValueError("Invalid token, expecting a ) on position {}".format(self.tokens.position))     
        else:
            raise ValueError("Invalid token, expecting a ( on position {}".format(self.tokens.position))     
        return result
        
    def parseExpression(self):
        result = self.parseTerm()
        while True:
            token = self.tokens.actual
            if token == None:
                break
            if token.type == "PLUS":
                second_value = self.parseTerm()
                result = BinOp("+", [result, second_value])
            elif token.type == "MINUS":
                second_value = self.parseTerm()
                result = BinOp("-", [result, second_value])
            else:
                break
        return result
    def parseTerm(self):
        result = self.parseFactor()
        while True:
            token = self.tokens.selectNext()
            if token == None:
                break
            elif token.type == "MULT":
                second_value = self.parseFactor()
                result = BinOp("*", [result, second_value])
            elif token.type == "DIV":
                second_value = self.parseFactor()
                result = BinOp("/", [result, second_value])
            else:
                break
        return result
    def parseFactor(self):
        token = self.tokens.selectNext()
        if token == None:
            raise ValueError("Invalid token, expecting a number or opening parentesis on position {}, got NULL".format(self.tokens.position))
        if token.type == "INT":
            result = IntVal(token.value, [])
        elif token.type == "OPEN_PAR":
            result = self.parseExpression()
            token = self.tokens.actual
            if token.type != "CLOSE_PAR":
                raise ValueError("Invalid token, missing parentesis close on position {}".format(self.tokens.position))
        elif token.type == "MINUS":
            result = self.parseFactor()
            result = UnOp("-", [result])
        elif token.type == "PLUS":
            result = self.parseFactor()
        elif token.type == "IDE":
            result = Identifier(token.value, [])
        else:
            raise ValueError("Invalid token, expecting number or opening parentesis on position {}".format(self.tokens.position))
        return result 
