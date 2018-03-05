from parser import Parser

def main():
        test = "+-+3*5"
        try:
            parser = Parser(test)
            result = parser.parseExpression()            
            print(result)   
        except ValueError as err:
            print(err)

main()
