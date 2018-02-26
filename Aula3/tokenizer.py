from token import Token

ALPHABET = ['0','1','2','3','4','5','6','7','8','9','+','-']

class Tokenizer():
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.alphabet = ALPHABET
    def selectNext(self):
        if self.position >= len(self.origin):
            return None
        char = self.origin[self.position]
        while char == ' ' and self.position:
            self.position += 1
            if self.position == len(self.origin):
                return None
            char = self.origin[self.position]
        if char not in self.alphabet:
            pass
            raise ValueError("Invalid Char")
        elif char.isdigit():
            number = char
            while True:
                self.position += 1
                if (self.position >= len(self.origin)):
                    break
                char = self.origin[self.position]
                if not char.isdigit():
                    break
                else:
                    number += char
            self.actual = Token('INT', int(number))
        else:
            if (char == '+'):
                self.actual = Token('PLUS', None)
            elif (char == '-'):
                self.actual = Token('MINUS', None)
            self.position += 1
        return self.actual
