import sys
#NEED DEBUGGING ESPICIALY FLAG AND JUMP FUNCTIONS

'''
0. FATAL ERROR IN ASSEMBLER MOVE DONT WORK FOR MULTIPLE TYPES
1. flag is printing in reverse
2. flag dont hold for consecutive changes

'''
# utility functions
def bintodeci(bin):
    ret = 0
    counter = 0
    max = len(bin)
    for i in bin:
        if(i == "1"):
            ret += 2**(max-counter-1)
        counter += 1
    return ret

def decitobin(deci):
    x = ["0"]*16
    d = deci
    i = 16
    while(d != 0 or i != 0):
        x[i-1] = str(d%2)
        d = d//2
        i -= 1
    y = ''.join(x)
    return y

#start of program

program_counter = 0
HLT_F = False

REGISTERS = [0]*8
for i in range(8):
    REGISTERS[i] = '0'*16

FLAG_R = {
    'V':0,
    'L':0,
    'G':0,
    'E':0,
    'written': False
}

def flag_set():
    x = ['0']*16
    x[0] = str(FLAG_R['E'])
    x[1] = str(FLAG_R['G'])
    x[2] = str(FLAG_R['L'])
    x[3] = str(FLAG_R['V'])
    REGISTERS[7] = ''.join(x)

MEMORY = [0]*256
for i in range(256):
    MEMORY[i] = "0"*16

# file input and parsing to be done here (assuming error free file).
def initialize():
    code = sys.stdin.read().strip()
    p_code = code.split("\n")
    for i in range(len(p_code)):
        MEMORY[i] = p_code[i]

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
    mem = bintodeci(code[8:16:])
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
    a = bintodeci(REGISTERS[code[1]]) + bintodeci(REGISTERS[code[2]])
    if(a >2*16):
        a = a%(2**16)
        FLAG_R['V'] = 1
        FLAG_R["written"] = True
        flag_set()
    REGISTERS[code[3]] = decitobin(a)
    return program_counter + 1 #

def sub(code):
    a = bintodeci(REGISTERS[code[1]]) - bintodeci(REGISTERS[code[2]])
    if(a < 0):
        a = 0
        FLAG_R['V'] = 1
        FLAG_R["written"] = True
        flag_set()
    REGISTERS[code[3]] = decitobin(a)
    return program_counter + 1 #

def movi(code):
    a = code[2]
    REGISTERS[code[1]] = decitobin(a)
    return program_counter + 1 #

def movr(code):
    a = REGISTERS[code[2]]
    REGISTERS[code[1]] = a
    return program_counter + 1 #

def ld(code):
    REGISTERS[code[1]] = MEMORY[code[2]]
    return program_counter + 1 #

def st(code):
    MEMORY[code[2]] = REGISTERS[code[1]]
    return program_counter + 1 #

def mul(code):
    a = bintodeci(REGISTERS[code[1]]) * bintodeci(REGISTERS[code[2]])
    if(a >2**16):
        a = REGISTERS[code[3]] % 2**16
    REGISTERS[code[3]] = decitobin(a)
    return program_counter + 1 #

def div(code):
    a = bintodeci(REGISTERS[code[1]]) // bintodeci(REGISTERS[code[2]])
    b = bintodeci(REGISTERS[code[1]]) %  bintodeci(REGISTERS[code[2]])
    REGISTERS[0] = decitobin(a)
    REGISTERS[1] = decitobin(b)
    return program_counter + 1 #

def rs(code):
    a = bintodeci(REGISTERS[code[1]]) // (2**code[2])
    REGISTERS[code[1]] = decitobin(a)
    return program_counter + 1 #

def ls(code):
    a = bintodeci(REGISTERS[code[1]]) * (2**code[2])
    if(a >2**16):
        a = a % 2**16
        FLAG_R['V'] = 1
        FLAG_R["written"] = True
        flag_set()
    REGISTERS[code[1]] = decitobin(a)
    return program_counter + 1 #

def xor(code):
    a = REGISTERS[code[1]]
    b = REGISTERS[code[2]]
    x = 0
    c = ['0']*16
    for i in range(16):
        x = (int(a[i]) and not(int(b[i]))) or (not(int(a[i])) and int(b[i]))
        c[i] = str[x]
    REGISTERS[3] = ''.join(c)
    return program_counter + 1 #

def Or(code):
    a = REGISTERS[code[1]]
    b = REGISTERS[code[2]]
    x = 0
    c = ['0']*16
    for i in range(16):
        x = (int(a[i])) or (int(b[i]))
        c[i] = str[x]
    REGISTERS[3] = ''.join(c)
    return program_counter + 1 #

def And(code):
    a = REGISTERS[code[1]]
    b = REGISTERS[code[2]]
    x = 0
    c = ['0']*16
    for i in range(16):
        x = (int(a[i])) and (int(b[i]))
        c[i] = str[x]
    REGISTERS[3] = ''.join(c)
    return program_counter + 1 #

def Not(code):
    a = REGISTERS[code[1]]
    c = ['0']*16
    x = 0
    for i in  range(16):
        c[i] = str(not(a[i]))
    REGISTERS[2] = ''.join(c)
    return program_counter + 1 #

def cmp(code):
    x = (bintodeci(REGISTERS[code[1]]))
    y = (bintodeci(REGISTERS[code[2]]))
    if(x == y):
        FLAG_R["E"] = 1
    elif(x > y):
        FLAG_R["G"] = 1
    else:
        FLAG_R["L"] = 1
    FLAG_R["written"] = True
    flag_set()
    return program_counter + 1 # partial

def jmp(code):
    PC = program_counter + 1
    PC= code[1]
    return PC

def jlt(code):
    PC = program_counter + 1
    if FLAG_R['L'] == 1:
        PC = code[1]
    return PC

def jgt(code):
    PC = program_counter + 1
    if FLAG_R["G"] == 1:
        PC = code[1]
    return PC

def je(code):
    PC = program_counter + 1
    if FLAG_R["E"] == 1:
        PC =code[1]
    return PC

def hlt(code):
    global HLT_F
    HLT_F = True
    return program_counter

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
    x = decoder(code)
    return isa_exe[x[0]](x)

def reg_dump():
    print(decitobin(program_counter),REGISTERS[0],REGISTERS[1],REGISTERS[2],REGISTERS[3],REGISTERS[4],REGISTERS[5],REGISTERS[6],REGISTERS[7])

def mem_dump():
    for i in MEMORY:
        print(i)


initialize()
while(not(HLT_F)):
    x = False
    if(FLAG_R["written"]):
        x = True
    code = MEMORY[program_counter]
    new_pc = exec(code)
    if(x):
        FLAG_R["E"] = 0
        FLAG_R["G"] = 0
        FLAG_R["L"] = 0
        FLAG_R["V"] = 0
        FLAG_R["written"] = False
        flag_set()
    reg_dump()
    program_counter = new_pc
mem_dump()


