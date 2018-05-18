from token import Token

PRINT, BEGIN, END, IF, THEN, ELSE, \
    WHILE, OR, AND, NOT, READ, PROGRAM, \
    VAR, INT, BOOLEAN, \
    TRUE, FALSE, DO, \
    FUNCTION = ('print', 'begin',
                'end', 'if', 'then',
                'else', 'while',
                'or', 'and', 'not', 'read',
                'program', 'var', 'int',
                'boolean', 'true', 'false', 'function', 'do')

ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-',
            '*', '/', '(', ')', ':', '=', ';', '<', '>', '!', '.', ',']
KEYWORDS = [PRINT, BEGIN, END, IF, THEN, ELSE, WHILE,
            OR, AND, NOT, READ, PROGRAM, VAR,
            INT, BOOLEAN, TRUE, FALSE, FUNCTION, DO]

TYPES = [INT, BOOLEAN]

BOOL = [TRUE, FALSE]


class Tokenizer():
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.alphabet = ALPHABET

    def selectNext(self):
        # Final do arquivo
        if self.position >= len(self.origin):
            self.actual = None
            return None
        char = self.origin[self.position]
        # Comentarios
        if char == '{':
            while char != '}':
                self.position += 1
                if self.position == len(self.origin):
                    return None
                char = self.origin[self.position]
            self.position += 1
            char = self.origin[self.position]
        # Espacos,enter e tabs
        while char.isspace() and self.position:
            self.position += 1
            if self.position == len(self.origin):
                return None
            char = self.origin[self.position]
        # Identificador
        if char.isalpha():
            identifier = char
            while True:
                self.position += 1
                if (self.position >= len(self.origin)):
                    break
                char = self.origin[self.position]
                if not char.isalpha() and not char.isdigit() and char != '_':
                    break
                else:
                    identifier += char
            if identifier in TYPES:
                self.actual = Token('TYPE', identifier)
            elif identifier in BOOL:
                self.actual = Token('boolean', identifier)
            elif identifier in KEYWORDS:
                self.actual = Token(identifier, None)
            else:
                self.actual = Token('IDE', identifier)
        # Caracter invalido
        elif char not in self.alphabet:
            raise ValueError("Invalid Char")
        # Digitos
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
            self.actual = Token('int', int(number))
        # Operacoes e parenteses
        else:
            if (char == '+'):
                self.actual = Token('PLUS', None)
            elif (char == '-'):
                self.actual = Token('MINUS', None)
            elif (char == '*'):
                self.actual = Token('MULT', None)
            elif (char == '/'):
                self.actual = Token('DIV', None)
            elif (char == '('):
                self.actual = Token('OPEN_PAR', None)
            elif (char == ')'):
                self.actual = Token('CLOSE_PAR', None)
            elif (char == ';'):
                self.actual = Token('SEMI_COLON', None)
            elif (char == ':'):
                if (self.position + 1 < len(self.origin)):
                    char = self.origin[self.position + 1]
                    if (char == '='):
                        self.actual = Token('ATRIBUTE', None)
                        self.position += 1
                    else:
                        self.actual = Token('VAR_DECLARATION', None)
            elif (char == '>'):
                self.actual = Token('COMP', ">")
            elif (char == '<'):
                self.actual = Token('COMP', "<")
            elif (char == '='):
                self.actual = Token('COMP', "=")
            elif (char == '!'):
                self.position += 1
                char = self.origin[self.position]
                if (char == '='):
                    self.actual = Token('COMP', "!=")
                else:
                    raise ValueError("Invalid Char")
            elif (char == '.'):
                self.actual = Token('END_PROGRAM', None)
            elif (char == ','):
                self.actual = Token('COMMA', None)
            self.position += 1
        return self.actual
