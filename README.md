# CompilerLogComp

Pascal simplified compiler written in python without external dependencies

# Features

To-do

# EBNF

```
program = "program", identifier, ";", block, ".";
functions = {"function", identifier, "(", var_dec, ")", ";", block};
block = [functions], ["var", var_dec], [statements];
var_dec = (identifier, {,",", identifier}, ":", type, ";")+
statements = "begin", statement, {";", statement}, "end";
statement = attribution | statements | print | if | while;
attribution = identifier, ":=", (expression | read);
print = "print", "(", expression, ")";
read = "read", "(", ")";
if = "if", rel_expression, "then", statement, ["else" statement"];
while = "while", rel_expression, "do", statement;
rel_expression = expression, {comp, expression};
expression = term, { ("+"|"-"|"or"), term, };
term = factor, { ("*" | "/" | "and"), factor };
factor = ("+" | "-" | "not"), (factor | number | boolean | ("(" expression ")") | identifier | func_call);
func_call = identifier, "(", [expression, {",", expression}], ")";
identifier = letter, {letter | digit | "_" };
comp = ">" | "<" | "=" | "!=";
number = digit+;
boolean = "true" | "false";
type = "int" | "boolean";
letter = [a-zA-Z];
digit = [0-9];
```

# SD (Syntatic Diagram)

![SD](https://raw.githubusercontent.com/marcelogdeandrade/CompilerLogComp/master/syntatic_diagram.png)
