# utility functions
def bintodeci(bin):
    ret = 0
    counter = 0
    max = len(bin)
    for i in bin:
        if(i == "1"):
            ret += 2**(max-counter)
        counter += 1
    return ret

#start of program
program_counter = 0
HLT_F = False

REGISTERS = []
for i in range(6):
    REGISTERS[i] = 0

MEMORY = []
for i in range(256):
    MEMORY[i] = "0"*16

# file input and parsing to be done here (assuming error free file).
#.
#.
#.

isa_type = {
    "10000":"A",
    "10001":"A",
    "10010":"B",
    "10011":"C",
    "10100":"D",
    "10101":"D",
    "10110":"A",
    "10111":"C",
    "11000":"B",
    "11001":"B",
    "11010":"A",
    "11011":"A",
    "11100":"A",
    "11101":"C",
    "11110":"C",
    "11111":"E",
    "01100":"E",
    "01101":"E",
    "01111":"E",
    "01010":"F",
}

def aparse(code):
    opcode = code[:5:]
    r1 = bintodeci(code[7:10:])
    r2 = bintodeci(code[10:13:])
    r3 = bintodeci(code[13:16:])
    return [opcode,r1,r2,r3]

def bparse(code):
    opcode = code[:5:]
    r1  = bintodeci(code[5:8:])
    Imm = bintodeci(code[8:16:])
    return [opcode,r1,Imm]

def cparse(code):
    opcode = code[:5:]
    r1 = bintodeci(code[10:13:])
    r2 = bintodeci(code[13:16:])
    return [opcode,r1,r2]

def dparse(code):
    opcode = code[:5:]
    r1  = bintodeci(code[5:8:])
    mem = bintodeci(code[8:16:])
    return [opcode,r1,mem]

def eparse(code):
    opcode = code[:5:]
    mem = bintodeci[8:16:]
    return [opcode,mem]

def fparse(code):
    opcode = code[:5:]
    return [opcode]


SYN_PARSE ={
    "A" : aparse,
    "B" : bparse,
    "C" : cparse,
    "D" : dparse,
    "E" : eparse,
    "F" : fparse,
} 

def decoder(code):
    # return format [<opcode>, arguments(decoded)....]  For eg. add r1 r2 r3 => ["10000",1,2,3]
    return SYN_PARSE[isa_type[code[:5:]]](code)
    

def add(code):
    return
def sub(code):
    return
def movi(code):
    return
def movr(code):
    return
def ld(code):
    return
def st(code):
    return
def mul(code):
    return
def div(code):
    return
def rs(code):
    return
def ls(code):
    return
def xor(code):
    return
def Or(code):
    return
def And(code):
    return
def Not(code):
    return
def cmp(code):
    return
def jmp(code):
    return
def jlt(code):
    return
def jgt(code):
    return
def je(code):
    return
def hlt(code):
    return

isa_exe = {
    "10000": add ,
    "10001": sub ,
    "10010": movi,
    "10011": movr,
    "10100": ld  ,
    "10101": st  ,
    "10110": mul ,
    "10111": div ,
    "11000": rs  ,
    "11001": ls  ,
    "11010": xor ,
    "11011": Or  ,
    "11100": And ,
    "11101": Not ,
    "11110": cmp ,
    "11111": jmp ,
    "01100": jlt ,
    "01101": jgt ,
    "01111": je  ,
    "01010": hlt ,
}

def exec(code):
    return