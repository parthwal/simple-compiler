'''
TO DO LIST:
1> REWRITE MEANINGFUL ERROR TYPE AND MESSAGE
2> IN TYPE C SYNTAX MOV FUNC CAN ALLOW FLAG REGISTER IN THE SECOND SLOT : NEED TO CODE THAT
3> TEST CODE 
4> WRITE BINARY PRINTER(NODE ALL INTANCES OF THE LABELS SHOULD BEL REPLACED WITH APROPRIATE MEMORY NUMBER, VARIABLES SHOULD BE PRESENT AT LAST)

baki kuch galti ho toh bta dena


'''
from shutil import ExecError


f = open("instructions.txt")
code = f.read().strip() #file input

MAX_NO = 255
MIN_NO = 0
MAX_MEM = 256


VAR_F  = True
HLT_F  = False
MEM_F  = False


isa_commands={
    "add" :"10000",
    "sub" :"10001",
    "movi":"10010",
    "movr":"10011",
    "ld"  :"10100",
    "st"  :"10101",
    "mul" :"10110",
    "div" :"10111",
    "rs"  :"11000",
    "ls"  :"11001",
    "xor" :"11010",
    "or"  :"11011",
    "and" :"11100",
    "not" :"11101",
    "cmp" :"11110",
    "jmp" :"11111",
    "jlt" :"01100",
    "jgt" :"01101",
    "je"  :"01111",
    "hlt" :"01010"
}

isa_type = {
    "add"  :"A",
    "sub"  :"A",
    "movi" :"B",
    "movr" :"C",
    "ld"   :"D",
    "st"   :"D",
    "mul"  :"A",
    "div"  :"C",
    "rs"   :"B",
    "ls"   :"B",
    "xor"  :"A",
    "or"   :"A",
    "and"  :"A",
    "not"  :"C",
    "cmp"  :"C",
    "jmp"  :"E",
    "jlt"  :"E",
    "jgt"  :"E",
    "je"   :"E",
    "hlt"  :"F",
    "var"  :"G",
}



REGISTERS = {
    "R0"   :"000",
    "R1"   :"001",
    "R2"   :"010",
    "R3"   :"011",
    "R4"   :"100",
    "R5"   :"101",
    "R6"   :"110",
    "FLAGS":"111"
}

labels = dict()
var    = dict()
line_counter = 0
parsed_code_temp = code.split("\n")
parsed_code = []




for i in parsed_code_temp:
    parsed_code.append(i.split())
print(parsed_code)

def initial_check(p_code):
    if len(p_code) > MAX_MEM:
        raise OverflowError("MEMORY LIMIT HAS REACHED")
    for i in p_code:
        if VAR_F:
            if i[0] != "var":
                VAR_F = False
        else:
            if i[0] == "var":
                raise ExecError("VARIABLES CAN ONLY DE DEFINED AT STARTING OF THE CODE")
        if HLT_F:
            raise NameError("HALT CAN ONLY BE CALLED AT THE END")
        else:
            if i[0] == "halt":
                HLT_F = True
            elif i[0][-1] == ":":
                if i[1] == "halt":
                    HLT_F = True

VAR_F  = True
HLT_F  = False
MEM_F  = False

def acheck(i):
    if len(i) == 4:
        for j in i[1::]:
            if j == "FLAGS":
                raise ValueError("FLAG REGISTER CANT BE USED WITH THIS COMMAND")
            if not(j in REGISTERS.keys()):
                raise ValueError("UNKNOWN REGISTER USED")
        line_counter += 1
        return True   
    raise TypeError("COMMAND DONT FOLLOW SYNTAX")

def bcheck(i):
    if len(i) == 3:
        if i[1] in REGISTERS.keys():
            if i[1] != "FLAGS":
                if i[2][0] == '$':
                    x = int(i[2][1::])
                    if(i <= MAX_NO and i >= MIN_NO):
                        line_counter += 1
                        return True
                    else:
                        raise OverflowError("IMMIDIATE VALUE OFF RANGE")
                else:
                    raise SyntaxError("EXPECTED A $ SIGN")
            else:
                raise ValueError("THIS OPPERATION CANT USE FLAG REGISTER")
        else:
            raise ValueError("INVALID REGISTER")
    else:
        raise SyntaxError("COMMAND DONT FOLLOW SYNTAX")

def ccheck(i):
    if len(i) == 3:
        for j in i[1::]:
            if j == "FLAGS":
                raise ValueError("FLAG REGISTER CANT BE USED WITH THIS COMMAND")
            if not(j in REGISTERS.keys()):
                raise ValueError("UNKNOWN REGISTER USED")
        line_counter += 1
        return True
    raise TypeError("COMMAND DONT FOLLOW SYNTAX")

def dcheck(i):
    if len(i) == 3:
        if i[1] in REGISTERS.keys():
            if i[1] != "FLAGS":
                if i[2] in var.keys():
                    line_counter += 1
                    return True
                else:
                    raise NotImplementedError("VARIABLE DOES NOT EXIST")
            else:
                raise ValueError("THIS OPERRATION CANT UUSE FLAG REGISTER")
        else:
            raise ValueError("INVALID REGISTER")
    else:
        raise SyntaxError("COMMAND DONT FOLLOW SYNTAX")

def echeck(i):
    if len(i) == 2:
        if i[1] in var:
            line_counter += 1
            return True
        else:
            raise NotImplementedError("VARIABLE DOES NOT EXIST")
    else:
        raise SyntaxError("COMMAND DONT FOLLOW SYNTAX")
def fcheck(i):
    if len(i) == 1:
        line_counter += 1
        return True
    else:
        raise SyntaxError("HALT CANT HAVE ARGUMENTS")
def gcheck(i):
    if VAR_F:
        if len(i) == 2:
            var[i[1]] = len(var)
            return True
        else:
            raise SyntaxError("INVALID SYNTAX")
    else:
        raise ExecError("LABELS CANT HAVE VAR COMMAND")




SYN_CHECK ={
    "A" : acheck,
    "B" : bcheck,
    "C" : ccheck,
    "D" : dcheck,
    "E" : echeck,
    "F" : fcheck,
    "G" : gcheck,
} 


def hcheck(i):
    if i[0][-1] == ':':
        if len(i) > 1:
            if i[1] != 'var':
                labels[i[0][:-1:]] = line_counter
                if i[1] in isa_type.keys():
                    SYN_CHECK[isa_type[i[1]]](i[1::])
                else:
                    raise SyntaxError("INVALID SYNTAX")
            else:
                raise ExecError("LABELS CANT HAVE VAR COMMAND")
        else:
            raise SyntaxError("INVALID SYNTAX")
    else:
        raise SyntaxError("INVALID SYNTAX")
        
      
def syntax_check(p_code):
    for i in p_code:
        if i[0] in isa_type.keys():
            SYN_CHECK[isa_type[i[0]]](i)
        else:
            hcheck(i)