from tokenizer import Tokenizer

class Parser():
    def __init__(self, origin):
        self.tokens = Tokenizer(origin)
    def parseExpression(self):
        token = self.tokens.selectNext()
        if token.type == "INT":
            result = token.value
            token = self.tokens.selectNext()
            while True:
                if token == None:
                    break
                elif token.type == "PLUS":
                    token = self.tokens.selectNext()
                    if token.type == "INT":
                        result += token.value
                    else:
                        raise ValueError("Invalid sum value")
                elif token.type == "MINUS":
                    token = self.tokens.selectNext()
                    if token.type == "INT":
                        result -= token.value
                    else:
                        raise ValueError("Invalid sub value")
                else:
                    raise ValueError("Invalid Token")
                token = self.tokens.selectNext()
        else:
            raise ValueError("Invalid Token")
        return result
