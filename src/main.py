from parser import Parser
from symbolTable import SymbolTable
from assembly import AssemblyCode


def percorrer_arvore(raiz):
    print(raiz.value)
    for i in raiz.children:
        percorrer_arvore(i)


def read_file(file_name):
    with open(file_name) as file:
        data = file.read()
    return data


def main():
        test = read_file("input3.txt")
        try:
            parser = Parser(test)
            symbolTable = SymbolTable(None)
            result = parser.parseProgram()
            # percorrer_arvore(result)
            result.Evaluate(symbolTable)
            print(AssemblyCode.assembly_code)
            AssemblyCode.writeFile("teste.asm")
        except ValueError as err:
            print(err)


main()
