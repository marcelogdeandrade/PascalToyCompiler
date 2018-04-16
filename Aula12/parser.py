from tokenizer import Tokenizer
from node import (BinOp, UnOp, IntVal, NoOp, Print,
                  Identifier, Statements, StrVal, If, While, Read)


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
                    raise ValueError("Invalid token, expecting a semi colon \
                        or a end on position {}".format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a begin on position {}"
                             .format(self.tokens.position))
        return result

    def parseStatement(self):
        token = self.tokens.selectNext()
        if token.type == "begin":
            result = self.parseStatements()
        elif token.type == "IDE":
            result = self.parseAtribution()
        elif token.type == "print":
            result = self.parsePrint()
        elif token.type == "if":
            result = self.parseIf()
        elif token.type == "while":
            result = self.parseWhile()
        else:
            raise ValueError("Invalid token, expecting a begin,identifier, print, if or while \
                             on position {}".format(self.tokens.position))
        return result

    def parseAtribution(self):
        value1 = StrVal(self.tokens.actual.value, [])
        token = self.tokens.selectNext()
        if (token.type == "ATRIBUTE"):
            token = self.tokens.selectNext()
            if (token.type == "read"):
                value2 = self.parseRead()
            else:
                value2 = self.parseExpression()
            result = BinOp(":=", [value1, value2])
        else:
            raise ValueError("Invalid token, expecting a := on position {}"
                             .format(self.tokens.position))
        return result

    def parsePrint(self):
        token = self.tokens.selectNext()
        if token.type == "OPEN_PAR":
            self.tokens.selectNext()
            value = self.parseExpression()
            token = self.tokens.actual
            if token.type == "CLOSE_PAR":
                result = Print(value, [value])
                self.tokens.selectNext()
            else:
                raise ValueError("Invalid token, expecting a ) on position {}"
                                 .format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a ( on position {}"
                             .format(self.tokens.position))
        return result

    def parseRelExpression(self):
        self.tokens.selectNext()
        value1 = self.parseExpression()
        token = self.tokens.actual
        if token.type == 'COMP':
            self.tokens.selectNext()
            value2 = self.parseExpression()
            result = BinOp(token.value, [value1, value2])
        else:
            raise ValueError("Invalid token, expecting a <, >, = or != \
                             on position {}".format(self.tokens.position))
        return result

    def parseIf(self):
        comp = self.parseRelExpression()
        token = self.tokens.actual
        if (token.type == "then"):
            self.tokens.selectNext()
            statement1 = self.parseStatements()
            token = self.tokens.actual
            if (token.type == "else"):
                self.tokens.selectNext()
                statement2 = self.parseStatements()
            else:
                statement2 = NoOp(None, [])
            result = If(None, [comp, statement1, statement2])
        else:
            raise ValueError("Invalid token, expecting a then on \
                             position {}".format(self.tokens.position))
        return result

    def parseRead(self):
        token = self.tokens.selectNext()
        if token.type == "OPEN_PAR":
            self.tokens.selectNext()
            token = self.tokens.actual
            if token.type == "CLOSE_PAR":
                result = Read(None, [])
                self.tokens.selectNext()
            else:
                raise ValueError("Invalid token, expecting a ) on position {}"
                                 .format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a ( on position {}"
                             .format(self.tokens.position))
        return result

    def parseWhile(self):
        comp = self.parseRelExpression()
        token = self.tokens.actual
        if (token.type == "then"):
            self.tokens.selectNext()
            statement1 = self.parseStatements()
            token = self.tokens.actual
            result = While(None, [comp, statement1])
        else:
            raise ValueError("Invalid token, expecting a then on \
                             position {}".format(self.tokens.position))
        return result

    def parseExpression(self):
        result = self.parseTerm()
        while True:
            token = self.tokens.actual
            if token is None:
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
            if token is None:
                break
            elif token.type == "MULT":
                self.tokens.selectNext()
                second_value = self.parseFactor()
                result = BinOp("*", [result, second_value])
            elif token.type == "DIV":
                self.tokens.selectNext()
                second_value = self.parseFactor()
                result = BinOp("/", [result, second_value])
            else:
                break
        return result

    def parseFactor(self):
        token = self.tokens.actual
        if token is None:
            raise ValueError("Invalid token, expecting a number or opening parentesis on \
                position {}, got NULL".format(self.tokens.position))
        if token.type == "INT":
            result = IntVal(token.value, [])
        elif token.type == "OPEN_PAR":
            self.tokens.selectNext()
            result = self.parseExpression()
            token = self.tokens.actual
            if token.type != "CLOSE_PAR":
                raise ValueError("Invalid token, missing parentesis close on \
                    position {}".format(self.tokens.position))
        elif token.type == "MINUS":
            self.tokens.selectNext()
            result = self.parseFactor()
            result = UnOp("-", [result])
        elif token.type == "PLUS":
            self.tokens.selectNext()
            result = self.parseFactor()
        elif token.type == "IDE":
            result = Identifier(token.value, [])
        else:
            raise ValueError("Invalid token, expecting number or opening parentesis on \
                position {}".format(self.tokens.position))
        return result
