# CompilerLogComp

Pascal simplified compiler written in python without external dependencies

**Project under development, updated version on last "Aula" folder**

# Features

To-do

# EBNF

```
program -> "program" identifier ";" {var_dec} {statements}
var_dec -> "var" (identifier {"," identifier} ":" type ";")+
statements -> "begin" statement {";" statement} "end";
statement -> attribution | statements | print | if | while;
attribution -> identifier ":=" (expression | read);
print -> "print" "(" expression ")";
read -> "read" "(" ")";
if -> "if" rel_expression "then" statements {"else" statements};
while -> "while" rel_expression "then" statements;
rel_expression -> expression comp expression;
expression -> term { ("+"|"-") term };
term -> factor { ("*" | "/") factor };
factor -> ("+" | "-") (factor | number | boolean | ("(" expression ")") | identifier);
identifier -> letter {letter | digit | "_" };
comp -> ">" | "<" | "=" | "!=";
number -> digit+;
boolean -> true | false;
type -> int | boolean;
letters -> [a-zA-Z];
digit -> [0-9];
```

# SD (Syntatic Diagram)

To-do