from parser import Parser
from symbolTable import SymbolTable


def percorrer_arvore(raiz):
    print(raiz.value)
    for i in raiz.children:
        percorrer_arvore(i)


def read_file(file_name):
    with open(file_name) as file:
        data = file.read()
    return data


def main():
        test = read_file("input.txt")
        try:
            parser = Parser(test)
            symbolTable = SymbolTable()
            result = parser.parseProgram()
            # percorrer_arvore(result)
            result.Evaluate(symbolTable)
        except ValueError as err:
            print(err)


main()
