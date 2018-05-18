from value import Value
from symbolTable import SymbolTable as SymbolTableClass
from id import Id
from assembly import AssemblyCode


class Node():
    def __init__(self, value, children):
        self.id = Id.getNewId()
        self.value = value
        self.children = children

    def Evaluate(self, SymbolTable, whileFlag=0):
        pass

    def generateAsm(self, SymbolTable, whileFlag):
        pass


class BinOp(Node):
    def same_type(self, value1, value2):
        if (value1.type == value2.type):
            return True
        else:
            return False

    def Evaluate(self, SymbolTable, whileFlag=0, nodeId=None):
        value1_obj = self.children[0].Evaluate(SymbolTable, whileFlag)
        self.generateAsm(SymbolTable, "push", whileFlag)
        value2_obj = self.children[1].Evaluate(SymbolTable, whileFlag)
        self.generateAsm(SymbolTable, "pop", whileFlag)
        value1 = value1_obj.getValue()
        value2 = value2_obj.getValue()
        if (self.value == "+"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_sum = value1 + value2
            self.generateAsm(SymbolTable, "ADD", whileFlag)
            result = Value("int")
            result.setValue(value_sum)
            return result
        elif (self.value == "-"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_sub = value1 - value2
            self.generateAsm(SymbolTable, "SUB", whileFlag)
            result = Value("int")
            result.setValue(value_sub)
            return result
        elif (self.value == "or"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_or = value1 or value2
            self.generateAsm(SymbolTable, "OR", whileFlag)
            result = Value("boolean")
            result.setValue(value_or)
            return result
        elif (self.value == "*"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_mult = value1 * value2
            self.generateAsm(SymbolTable, "IMUL", whileFlag)
            result = Value("int")
            result.setValue(value_mult)
            return result
        elif (self.value == "/"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_div = value1 // value2
            result = Value("int")
            self.generateAsm(SymbolTable, "DIV", whileFlag)
            result.setValue(value_div)
            return result
        elif (self.value == "and"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_and = value1 and value2
            self.generateAsm(SymbolTable, "AND", whileFlag)
            result = Value("boolean")
            result.setValue(value_and)
            return result
        elif (self.value == ">"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            self.generateAsm(SymbolTable, "jg", whileFlag, nodeId)
            value_bigger = value1 > value2
            result = Value("boolean")
            result.setValue(value_bigger)
            return result
        elif (self.value == "<"):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            self.generateAsm(SymbolTable, "jl", whileFlag, nodeId)
            value_smaller = value1 < value2
            result = Value("boolean")
            result.setValue(value_smaller)
            return result
        elif (self.value == "="):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            self.generateAsm(SymbolTable, "je", whileFlag, nodeId)
            value_equal = value1 == value2
            result = Value("boolean")
            result.setValue(value_equal)
            return result
        elif (self.value == "!="):
            if not self.same_type(value1_obj, value2_obj):
                raise ValueError("Operands must be the same type")
            value_diff = value1 != value2
            result = Value("boolean")
            result.setValue(value_diff)
            return result
        else:
            return

    def generateAsm(self, SymbolTable, op, whileFlag, nodeId=None):
        if not whileFlag:
            asm = ""
            if op == "push":
                asm += "PUSH EBX \n"
            elif op == "pop":
                asm += "POP EAX \n"
            elif op == "jl":
                asm += "CMP EAX, EBX \n"
                asm += "CALL binop_jl \n"
                asm += "CMP EBX, False \n"
                asm += "JE EXIT_{0} \n".format(nodeId)
            elif op == "jg":
                asm += "CMP EAX, EBX \n"
                asm += "CALL binop_jg \n"
                asm += "CMP EBX, False \n"
                asm += "JE EXIT_{0} \n".format(nodeId)
            elif op == "je":
                asm += "CMP EAX, EBX \n"
                asm += "CALL binop_je \n"
                asm += "CMP EBX, False \n"
                asm += "JE EXIT_{0} \n".format(nodeId)
            elif op == "IMUL":
                asm += "IMUL EBX \n"
                asm += "MOV EBX, EAX \n"
            else:
                asm += "{0} EBX, EAX \n".format(op)
            AssemblyCode.assembly_code += asm


class Assignment(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        name = self.children[0].Evaluate(SymbolTable, whileFlag).getValue()
        value = self.children[1].Evaluate(SymbolTable, whileFlag).getValue()
        self.generateAsm(SymbolTable, whileFlag)
        SymbolTable.setSymbol(name, value)

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            value1 = self.children[0].Evaluate(
                SymbolTable, whileFlag).getValue()
            value2 = SymbolTable.id
            asm = "MOV [{0}_{1}], EBX \n".format(value1, value2)
            AssemblyCode.assembly_code += asm


class UnOp(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        value_obj = self.children[0].Evaluate(SymbolTable, whileFlag)
        value = value_obj.getValue()
        if (self.value == "-"):
            result = Value("int")
            result.setValue(value * -1)
            return result
        elif (self.value == "not"):
            if value_obj.type == "boolean":
                result = Value("boolean")
                result.setValue(not value)
                return result
            else:
                raise ValueError("Operand must be a boolean")
        else:
            return


class StrVal(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        value = Value("string")
        value.setValue(self.value)
        return value


class IntVal(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        self.generateAsm(SymbolTable, whileFlag)
        value = Value("int")
        value.setValue(self.value)
        return value

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            asm = "MOV EBX, {0} \n".format(self.value)
            AssemblyCode.assembly_code += asm


class BoolVal(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        self.generateAsm(SymbolTable, whileFlag)
        value = Value("boolean")
        value.setValue(self.value)
        return value

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            asm = "MOV EBX, ${0} \n".format(self.value)
            AssemblyCode.assembly_code += asm


class Identifier(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        self.generateAsm(SymbolTable, whileFlag)
        value = SymbolTable.getSymbol(self.value)
        return value

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            asm = "MOV EBX, [{0}_{1}] \n".format(self.value, SymbolTable.id)
            AssemblyCode.assembly_code += asm


class NoOp(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        return None


class Statements(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        for child in self.children:
            child.Evaluate(SymbolTable, whileFlag)


class Print(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        value = self.children[0].Evaluate(SymbolTable, whileFlag)
        self.generateAsm(SymbolTable, whileFlag)
        print(value.getValue())

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            asm = "PUSH EBX \n"
            asm += "CALL print \n"
            AssemblyCode.assembly_code += asm


class Read(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        result = input()
        value = Value("int")
        value.setValue(int(result))
        return value


class If(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        comp = self.children[0].Evaluate(SymbolTable, whileFlag, self.id)
        if (comp.value):
            self.children[1].Evaluate(SymbolTable, whileFlag)
        else:
            self.children[2].Evaluate(SymbolTable, whileFlag)

    def generateAsm(self, SymbolTable):
        pass


class While(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        comp = self.children[0]
        self.generateAsm(SymbolTable, "LOOP", whileFlag, "declare")
        flag = 0
        while (comp.Evaluate(SymbolTable, flag, self.id).getValue()):
            self.children[1].Evaluate(SymbolTable, flag)
            flag = 1
        self.generateAsm(SymbolTable, "JMP LOOP", whileFlag, "jump")
        self.generateAsm(SymbolTable, "EXIT", whileFlag, "declare")

    def generateAsm(self, SymbolTable, label, whileFlag, op):
        if not whileFlag:
            if op == "declare":
                asm = "{0}_{1}: \n".format(label, self.id)
                AssemblyCode.assembly_code += asm
            else:
                asm = "{0}_{1} \n".format(label, self.id)
                AssemblyCode.assembly_code += asm


class Program(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        self.generateAssemblyConstants()
        SymbolTable.createSymbol(self.value, None)
        for i in range(len(self.children)):
            if i == 2:  # Statements
                self.generateAsm(SymbolTable, whileFlag)
            self.children[i].Evaluate(SymbolTable, whileFlag)
        self.generateEndInterruption()

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            asm = """
    section .text
        global _start

    print:  ; subrotina print
      POP EBX
      POP EAX
      PUSH EBX
      XOR ESI, ESI

    print_dec:
      MOV EDX, 0
      MOV EBX, 0x000A
      DIV EBX
      ADD EDX, '0'
      PUSH EDX
      INC ESI
      CMP EAX, 0
      JZ print_next
      JMP print_dec

    print_next:
      CMP ESI, 0
      JZ print_exit
      DEC ESI

      MOV EAX, SYS_WRITE
      MOV EBX, STDOUT

      POP ECX
      MOV [res], ECX
      MOV ECX, res

      MOV EDX, 1
      INT 0x80
      JMP print_next

    print_exit:
      RET

    ; subrotinas if/while
    binop_je:
      JE binop_true
      JMP binop_false

    binop_jg:
      JG binop_true
      JMP binop_false

    binop_jl:
      JL binop_true
      JMP binop_false

    binop_false:
      MOV EBX, False
      JMP binop_exit
    binop_true:
      MOV EBX, True
    binop_exit:
      RET

"""
            asm += "_start: \n"
            AssemblyCode.assembly_code += asm

    def generateAssemblyConstants(self):
        asm = ""
        asm += "; constantes \n"
        asm += "SYS_EXIT equ 1 \n"
        asm += "SYS_READ equ 3 \n"
        asm += "SYS_WRITE equ 4 \n"
        asm += "STDIN equ 0 \n"
        asm += "STDOUT equ 1 \n"
        asm += "True equ 1 \n"
        asm += "False equ 0 \n"
        asm += "segment .data \n"
        AssemblyCode.assembly_code += asm

    def generateEndInterruption(self):
        asm = "MOV EAX, 1 \n"
        asm += "INT 0x80"
        AssemblyCode.assembly_code += asm


class VarDec(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        value1_obj = self.children[0].Evaluate(SymbolTable, whileFlag)
        value2_obj = self.children[1].Evaluate(SymbolTable, whileFlag)
        value1 = value1_obj.getValue()
        value2 = value2_obj.getValue()
        SymbolTable.createSymbol(value1, value2)
        self.generateAsm(SymbolTable, whileFlag)

    def generateAsm(self, SymbolTable, whileFlag):
        if not whileFlag:
            value1 = self.children[0].Evaluate(
                SymbolTable, whileFlag).getValue()
            asm = "{0}_{1} RESD 1 \n".format(value1, SymbolTable.id)
            AssemblyCode.assembly_code += asm


class MultiVarDec(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        self.generateAsm(SymbolTable, whileFlag, "init")
        for child in self.children:
            child.Evaluate(SymbolTable, whileFlag)
        self.generateAsm(SymbolTable, whileFlag, "res")

    def generateAsm(self, SymbolTable, whileFlag, op):
        if not whileFlag:
            if op == "init":
                asm = "segment .bss ; variaveis \n"
                AssemblyCode.assembly_code += asm
            else:
                asm = "res RESB 1"
                AssemblyCode.assembly_code += asm


class FuncDec(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        SymbolTable.createSymbol(self.value, "func")
        SymbolTable.setSymbol(self.value, self)


class Funcs(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        for func in self.children:
            func.Evaluate(SymbolTable, whileFlag)


class FuncCall(Node):
    def Evaluate(self, SymbolTable, whileFlag=0):
        func_name = self.value
        func_node = SymbolTable.getSymbol(func_name, "func").getValue()
        funcSymbolTable = SymbolTableClass(SymbolTable)
        var_dec = func_node.children[0]
        args = [x.children[0] for x in var_dec.children]
        func_node.children[0].Evaluate(funcSymbolTable, whileFlag)
        if (len(args) != len(self.children)):
            raise ValueError("Number of arguments must \
                              be the same as declaration")
        for i in range(len(args)):
            symbol = args[i].Evaluate(funcSymbolTable, whileFlag).getValue()
            symbol_type = funcSymbolTable.getSymbol(symbol).getType()
            value_obj = self.children[i].Evaluate(SymbolTable, whileFlag)
            if (symbol_type != value_obj.getType()):
                raise ValueError("Function argument must be \
                                   the same as declared")
            value = value_obj.getValue()
            funcSymbolTable.setSymbol(symbol, value)
        for i in range(1, len(func_node.children)):
            func_node.children[i].Evaluate(funcSymbolTable, whileFlag)
        result = funcSymbolTable.getSymbol(func_name)
        return result
