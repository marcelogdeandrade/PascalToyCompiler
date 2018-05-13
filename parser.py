from tokenizer import Tokenizer
from node import (BinOp, UnOp, IntVal, NoOp, Print,
                  Identifier, Statements, StrVal, If,
                  While, Read, Program, VarDec, BoolVal,
                  FuncDec, Funcs, FuncCall)


class Parser():
    def __init__(self, origin):
        self.tokens = Tokenizer(origin)
        self.tokens.selectNext()

    def parseProgram(self):
        token = self.tokens.actual
        if token.type == "program":
            token = self.tokens.selectNext()
            if token.type == "IDE":
                name_program = token.value
                token = self.tokens.selectNext()
                if token.type == "SEMI_COLON":
                    self.tokens.selectNext()
                    variables = self.parseVariables()
                    functions = self.parseFunctions()
                    statements = self.parseStatements()
                    result = Program(name_program,
                                     [variables, functions, statements])
                    token = self.tokens.actual
                    if token.type == "END_PROGRAM":
                        pass
                    else:
                        raise ValueError("Invalid token, expecting a . on position \
                                         {}".format(self.tokens.position))
                else:
                    raise ValueError("Invalid token, expecting a semi colon \
                        or a end on position {}".format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a program on \
                             position {}".format(self.tokens.position))
        return result

    def parseFunctionCall(self):
        pass

    def parseFunctions(self):
        token = self.tokens.actual
        result = Funcs(None, [])
        while True:
            if token.type == "function":
                token = self.tokens.selectNext()
                if token.type == "IDE":
                    function_name = token.value
                    func = FuncDec(function_name, [])
                    self.tokens.selectNext()
                    arguments = self.parseArgumentsFunction(function_name)
                    self.tokens.selectNext()
                    variables = self.parseVariables()
                    functions = self.parseFunctions()
                    statements = self.parseStatements()
                    func.children.append(arguments)
                    func.children.append(variables)
                    func.children.append(functions)
                    func.children.append(statements)
                    result.children.append(func)
                    token = self.tokens.actual
                else:
                    raise ValueError("Invalid token, expecting a identifier on position \
                                         {}".format(self.tokens.position))
            elif token.type == "begin":
                return result
            else:
                raise ValueError("Invalid token, expecting a function on position \
                                     {}".format(self.tokens.position))

    def parseArgumentsFunction(self, function_name):
        token = self.tokens.actual
        if token.type == "OPEN_PAR":
            list_arguments = []
            while True:
                token = self.tokens.selectNext()
                if token.type == "IDE":
                    list_arguments.append(token.value)
                    token = self.tokens.selectNext()
                    if token.type == "VAR_DECLARATION":
                        break
                    elif token.type == "COMMA":
                        pass
                    else:
                        raise ValueError("Invalid token, expecting a : or , on position \
                             {}".format(self.tokens.position))
                else:
                    raise ValueError("Invalid token, expecting a identifier on position \
                             {}".format(self.tokens.position))
            token = self.tokens.selectNext()
            if token.type == "TYPE":
                arguments = VarDec(None, [])
                for var_name in list_arguments:
                    var_name = StrVal(var_name, [])
                    value = StrVal(token.value, [])
                    variable = BinOp(":", [var_name, value])
                    arguments.children.append(variable)
                token = self.tokens.selectNext()
                if token.type == "CLOSE_PAR":
                    token = self.tokens.selectNext()
                    if token.type == "VAR_DECLARATION":
                        token = self.tokens.selectNext()
                        if token.type == "TYPE":
                            return_var_name = StrVal(function_name, [])
                            return_type = StrVal(token.value, [])
                            variable = BinOp(":", [return_var_name,
                                                   return_type])
                            arguments.children.append(variable)
                            token = self.tokens.selectNext()
                            if token.type == "SEMI_COLON":
                                return arguments
                            else:
                                raise ValueError("Invalid token, expecting a ; on position \
                             {}".format(self.tokens.position))
                        else:
                            raise ValueError("Invalid token, expecting a type on position \
                             {}".format(self.tokens.position))
                    else:
                        raise ValueError("Invalid token, expecting a : on position \
                             {}".format(self.tokens.position))
                else:
                    raise ValueError("Invalid token, expecting a ) on position \
                             {}".format(self.tokens.position))
            else:
                raise ValueError("Invalid token, expecting a type on position \
                             {}".format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a ( on position \
                             {}".format(self.tokens.position))

    def parseVariables(self):
        token = self.tokens.actual
        result = VarDec(None, [])
        if token.type != "begin":
            if token.type == "var":
                token = self.tokens.selectNext()
                while True:
                    list_vars = []
                    while True:
                        if token.type == "IDE":
                            list_vars.append(token.value)
                            token = self.tokens.selectNext()
                            if token.type == "COMMA":
                                token = self.tokens.selectNext()
                            elif token.type == "VAR_DECLARATION":
                                break
                            else:
                                raise ValueError("Invalid token, expecting a , or : on position \
                                     {}".format(self.tokens.position))
                        else:
                            raise ValueError("Invalid token, expecting a identifier on position \
                                     {}".format(self.tokens.position))
                    token = self.tokens.selectNext()
                    if token.type == "TYPE":
                        for var_name in list_vars:
                            var_name = StrVal(var_name, [])
                            value = StrVal(token.value, [])
                            variable = BinOp(":", [var_name, value])
                            result.children.append(variable)
                        token = self.tokens.selectNext()
                        if token.type == "SEMI_COLON":
                            token = self.tokens.selectNext()
                            if token.type == "begin":
                                break
                            elif token.type == "function":
                                break
                            elif token.type == "IDE":
                                pass
                            else:
                                raise ValueError("Invalid token, expecting a begin \
                                                 or identifier on position {}"
                                                 .format(self.tokens.position))
                        else:
                            raise ValueError("Invalid token, expecting a ; on position \
                                             {}".format(self.tokens.position))
                    else:
                        raise ValueError("Invalid token, expecting a type on position \
                                 {}".format(self.tokens.position))
            else:
                raise ValueError("Invalid token, expecting a var on position \
                                 {}".format(self.tokens.position))
        return result

    def parseStatements(self):
        token = self.tokens.actual
        if token.type == "begin":
            result = Statements(None, [])
            while True:
                self.tokens.selectNext()
                result.children.append(self.parseStatement())
                token = self.tokens.actual
                if token.type == "SEMI_COLON":
                    pass
                elif token.type == "end":
                    break
            if self.tokens.actual.type == "end":
                self.tokens.selectNext()
                pass
            else:
                raise ValueError("Invalid token, expecting a end on \
                                 position {}".format(self.tokens.position))
        else:
            raise ValueError("Invalid token, expecting a begin on \
                                 position {}".format(self.tokens.position))
        return result

    def parseStatement(self):
        token = self.tokens.actual
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
            statement1 = self.parseStatement()
            token = self.tokens.actual
            if (token.type == "else"):
                self.tokens.selectNext()
                statement2 = self.parseStatement()
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
            statement1 = self.parseStatement()
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
                self.tokens.selectNext()
                second_value = self.parseTerm()
                result = BinOp("+", [result, second_value])
            elif token.type == "MINUS":
                self.tokens.selectNext()
                second_value = self.parseTerm()
                result = BinOp("-", [result, second_value])
            elif token.type == "or":
                self.tokens.selectNext()
                second_value = self.parseTerm()
                result = BinOp("or", [result, second_value])
            else:
                break
        return result

    def parseTerm(self):
        result = self.parseFactor()
        while True:
            token = self.tokens.actual
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
            elif token.type == "and":
                self.tokens.selectNext()
                second_value = self.parseFactor()
                result = BinOp("and", [result, second_value])
            else:
                break
        return result

    def parseFactor(self):
        token = self.tokens.actual
        if token is None:
            raise ValueError("Invalid token, expecting a number or opening parentesis on \
                position {}, got NULL".format(self.tokens.position))
        if token.type == "int":
            result = IntVal(token.value, [])
            self.tokens.selectNext()
        elif token.type == "boolean":
            result = BoolVal(token.value, [])
            self.tokens.selectNext()
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
        elif token.type == "not":
            self.tokens.selectNext()
            result = self.parseFactor()
            result = UnOp("not", [result])
        elif token.type == "PLUS":
            self.tokens.selectNext()
            result = self.parseFactor()
        elif token.type == "IDE":
            identifier = token.value
            token = self.tokens.selectNext()
            if token.type == "OPEN_PAR":
                token = self.tokens.selectNext()
                args = []
                while True:
                    if token.type == "CLOSE_PAR":
                        break
                    else:
                        arg = self.parseExpression()
                        args.append(arg)
                        token = self.tokens.actual
                        if token.type == "COMMA":
                            self.tokens.selectNext()
                            pass
                        elif token.type == "CLOSE_PAR":
                            break
                        else:
                            raise ValueError("Invalid token, expecting a , or ) on \
                                    position {}".format(self.tokens.position))
                none_value = IntVal(None, [])
                args.append(none_value)
                result = FuncCall(identifier, args)
                self.tokens.selectNext()
            else:
                result = Identifier(identifier, [])
        else:
            raise ValueError("Invalid token, expecting number or opening parentesis on \
                position {}".format(self.tokens.position))
        return result
