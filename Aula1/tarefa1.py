def do_equation(equation):
    result = 0
    parsed_str = '+'
    #Splits equation on numbers and sign
    for i in equation:
        if (i == '+' or i == '-' or i == '*' or i == '/'):
            parsed_str += ','
            parsed_str += i
        if (i.isdigit()):
            parsed_str += i
    parsed_str = parsed_str.split(',')
    #Sums all numbers based on signs
    for i in parsed_str:
        if (i[0] == '+'):
            result += str_to_int(i[1:])
        elif (i[0] == '-'):
            result -= str_to_int(i[1:])
        elif (i[0] == '*'):
            result *= str_to_int(i[1:])
        elif (i[0] == '/'):
            result /= str_to_int(i[1:])
    return result

def str_to_int(number):
    result = 0
    number = number[::-1]
    for i in range(len(number)):
        result += int(number[i]) * 10**i
    return result

equation = str(input())
print('Resultado:')
print(do_equation(equation))