import sys
#NEED DEBUGGING ESPICIALY FLAG AND JUMP FUNCTIONS

'''
0. FATAL ERROR IN ASSEMBLER MOVE DONT WORK FOR MULTIPLE TYPES
0. FATAL ERROR IN ASSEMBLER RS LS PROVIDING WRONG OUTPUT
1. flag is printing in reverse ==
2. flag dont hold for consecutive changes ==
3. something wrong wirh ls and rs ==
4. all logical operations are broken ==
5. check for harder test case with multiple things hapenning
6. fix PC val ==
7. check jump instructions
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


inp="193.2"

    

def CSEToDec(reg):
    cse_rep=reg[8::]
    # print(cse_rep)
    exponent=cse_rep[:3:]
    mantissa=cse_rep[3::]
    # print(exponent,mantissa)
    exponent=int(exponent,2)+1
    # print(exponent)
    first=f'1{mantissa[:exponent-1:]}'
    second=mantissa[exponent-1::]
    # print(first,'.',second)
    pre_dec=int(first,2)
    # print(pre_dec)
    temp=second[::-1]
    sum=0
    for i in temp:
        sum=(sum+int(i))/2
    post_dec=float(f'{sum}')
    out=pre_dec+post_dec
    # print(out)
    return(out)

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
    x[15] = str(FLAG_R['E'])
    x[14] = str(FLAG_R['G'])
    x[13] = str(FLAG_R['L'])
    x[12] = str(FLAG_R['V'])
    REGISTERS[7] = ''.join(x)

def decToCSE(inp):
    # print(inp)
    if '.' not in inp:
        # print("Integer value does not require cse112 floating point representation")
        # exit()
        inp+='.0'
    if float(inp)<1:
        # print("Can't store values under 1") #overplow clamp to 0
        # exit()
        inp = '0.0'
        FLAG_R['V'] = 1
        FLAG_R["written"] = True
        flag_set()
    num=inp.split(".")
    # print(num)
    pre_dec=num[0]
    post_dec=num[1]
    first=bin(int(pre_dec)).replace('0b','')
    # print(first)
    second=float(f'0.{post_dec}')
    # print(second)
    temp=''
    while len(temp)<5:
        second*=2
        if second>1:
            second-=1
            temp+='1'
        elif second<1:
            temp+='0'
        elif second==1:
            temp+='1'
            break
    # print(temp)
    second=temp
    # print(f'{first}.{second}')
    mantissa=f'{first[1::]}{second}'
    # print(mantissa)
    # if len(mantissa)>5:
        
    #     # print("Mantissa longer than 5, Truncating till 5 digits")
    mantissa=mantissa[:5:]
    # print(mantissa)
    exponent=len(str(first))
    # print(exponent)
    if exponent>7:
        FLAG_R['V'] = 1
        FLAG_R["written"] = True
        flag_set()
        # print("Overflow: Exponent Greater than 7")
    exponent=bin(exponent-1).replace('0b','')
    if(len(exponent) > 3):
        exponent=exponent[-3::]
    # print(exponent)
    while len(exponent)<3:
        exponent=f'0{exponent}'
    while len(mantissa)<5:
        mantissa=f'{mantissa}0'
    # print(exponent,mantissa)
    cse_rep=exponent+mantissa
    # print(cse_rep)
    cse_rep='00000000'+cse_rep
    # print(cse_rep)
    return(cse_rep)

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
    "00000":"A",
    "00001":"A",
    "00010":"B1"
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

def b1parse(code):
    opcode = code[:5:]
    r1  = bintodeci(code[5:8:])
    Imm = float(CSEToDec(code[:16:]))
    return [opcode,r1,Imm]

SYN_PARSE ={
    "A" : aparse,
    "B" : bparse,
    "C" : cparse,
    "D" : dparse,
    "E" : eparse,
    "F" : fparse,
    "B1": b1parse,
} 

def decoder(code):
    # return format [<opcode>, arguments(decoded)....]  For eg. add r1 r2 r3 => ["10000",1,2,3]
    return SYN_PARSE[isa_type[code[:5:]]](code)
    

def add(code):
    a = bintodeci(REGISTERS[code[1]]) + bintodeci(REGISTERS[code[2]])
    if(a >2**16):
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
    a = REGISTERS[code[1]]
    REGISTERS[code[2]] = a
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
        x = (bool(int(a[i])) and not(bool(int(b[i])))) or (not(bool(int(a[i]))) and bool(int(b[i])))
        c[i] = str(int(x))
    REGISTERS[code[3]] = ''.join(c)
    return program_counter + 1 #

def Or(code):
    a = REGISTERS[code[1]]
    b = REGISTERS[code[2]]
    x = 0
    c = ['0']*16
    for i in range(16):
        x = (bool(int(a[i]))) or (bool(int(b[i])))
        c[i] = str(int(x))
    REGISTERS[code[3]] = ''.join(c)
    return program_counter + 1 #

def And(code):
    a = REGISTERS[code[1]]
    b = REGISTERS[code[2]]
    x = 0
    c = ['0']*16
    for i in range(16):
        x = (bool(int(a[i]))) and (bool(int(b[i])))
        c[i] = str(int(x))
    REGISTERS[code[3]] = ''.join(c)
    return program_counter + 1 #

def Not(code):
    a = REGISTERS[code[1]]
    c = ['0']*16
    x = 0
    for i in  range(16):
        c[i] = str(int(not(bool(int(a[i])))))
    REGISTERS[code[2]] = ''.join(c)
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

def addf(code):
    a = float(CSEToDec(REGISTERS[code[1]])) + float(CSEToDec(REGISTERS[code[2]]))
    REGISTERS[code[3]] = decToCSE(str(a))
    return program_counter + 1

def subf(code):
    a = float(CSEToDec(REGISTERS[code[1]])) - float(CSEToDec(REGISTERS[code[2]]))
    REGISTERS[code[3]] = decToCSE(str(a))
    return program_counter + 1

def movf(code):
    a = code[2]
    REGISTERS[code[1]] = decToCSE(str(a))
    return program_counter + 1
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
    "00000": addf,
    "00001": subf,
    "00010": movf
}

def exec(code):
    x = decoder(code)
    return isa_exe[x[0]](x)

def reg_dump():
    print(decitobin(program_counter)[8:16],REGISTERS[0],REGISTERS[1],REGISTERS[2],REGISTERS[3],REGISTERS[4],REGISTERS[5],REGISTERS[6],REGISTERS[7])

def mem_dump():
    for i in MEMORY:
        sys.stdout.write(i)
        sys.stdout.write('\n')


initialize()
while(not(HLT_F)):
    code = MEMORY[program_counter]
    new_pc = exec(code)
    if(FLAG_R["written"]):
        FLAG_R["written"] = False
        flag_set()
    else:
        FLAG_R["E"] = 0
        FLAG_R["G"] = 0
        FLAG_R["L"] = 0
        FLAG_R["V"] = 0
        FLAG_R["written"] = False
        flag_set()
    reg_dump()
    program_counter = new_pc
mem_dump()


