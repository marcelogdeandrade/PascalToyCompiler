from parser import Parser


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
            result = parser.parseExpression()            
            # percorrer_arvore(result)
            print(result.Evaluate())
        except ValueError as err:
            print(err)

main()

