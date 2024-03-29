from shutil import ExecError
import sys
#file input
# f = open("instructions.txt")
# code=f.read().strip()
# f.close()
code = sys.stdin.read().strip()
code.replace(" ","")
code.replace("\n","")
#print(code)

MAX_NO = 255
MIN_NO = 0
MAX_MEM = 256

VAR_F  = True
HLT_F  = False
MEM_F  = False
MOV_TYPE=''

line_counter = 0

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
    "hlt" :"01010",
    "addf":"00000",
    "subf":"00001",
    "movf":"00010"
}

isa_type = {
    "add"  :"A",
    "sub"  :"A",
    "mov"  :"X",
    # "movi" :"B",
    # "movr" :"C",
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
    "addf" :"A",
    "subf" :"A",
    "movf" :"B"
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

def decToCSE(inp):
    # print(inp)
    if '.' not in inp:
        print("Integer value does not require cse112 floating point representation")
        # exit()
        inp+='.0'
    if float(inp)<1:
        print("Can't store values under 1")
        exit()
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
    exponent=len(str(first))
    # print(exponent)
    if exponent>7:
        print("Overflow: Exponent Greater than 7")
    if exponent<7:
        mantissa=f'{first[1::]}{second}'
    else:
        mantissa=f'{first[-7::]}{second}'
    # print(mantissa)
    exponent=bin(exponent-1).replace('0b','')
    if len(mantissa)>5:
        print("Mantissa longer than 5, Truncating till 5 digits")
    mantissa=mantissa[:5:]
    # print(mantissa)
    # if len(exponent)>3:
        # exponent=exponent[-3::]
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

labels = dict()
var    = dict()
parsed_code_temp = code.split("\n")
parsed_code = []

for i in parsed_code_temp:
    if i==" " or i=='\n' or i=="" or i==None:
        continue
    parsed_code.append(i.split())
    # print(parsed_code)
    # if 'label' in i.lower():
    #     i[1].lower()
    #     parsed_code.append(i.split()[1::])
    # if 'label' not in i.lower():
    #     i[0].lower()
    #     
# print(parsed_code)

f=open('printBinary.txt','w')

def initial_check(p_code):
    global VAR_F
    hLT_F = False
    line_c = 0
    if len(p_code) > MAX_MEM:
        # print(": ")
        print('MEMORY LIMIT REACHED')
        print(line_counter+1)
        raise OverflowError("MEMORY LIMIT REACHED")
    for i in range(len(p_code)):
        if len(p_code[i]) == 0:
            # print(p_code[i])
            continue
        if VAR_F:
            if p_code[i][0] != "var":
                VAR_F = False
                # continue
        else:
            if p_code[i][0] == "var":
                # print(": ")
                print('VARIABLES CAN ONLY DE DEFINED AT STARTING OF THE CODE')
                print(line_counter+1)
                raise ExecError("VARIABLES CAN ONLY DE DEFINED AT STARTING OF THE CODE")
        
        if p_code[i][0][-1] == ':':
            labels[p_code[i][0][:-1:]] = line_c
        
        if hLT_F:
            # print(": ")
            print('HALT CAN ONLY BE CALLED AT THE END')
            print(line_counter+1)
            raise NameError("HALT CAN ONLY BE CALLED AT THE END")
        else:
            if p_code[i][0] == "hlt":
                hLT_F = True
                continue
            elif p_code[i][0][-1] == ":":
                try:
                    if p_code[i][1] == "hlt":
                        hLT_F = True
                        continue
                except IndexError:
                    print(line_c)
                    raise IndexError("EMPTY LABEL CANT BE USED")
        line_c += 1

    if(p_code[-1][0] != "hlt"):
        if(p_code[-1][0][-1] == ':'):
            if p_code[-1][1] == "hlt":
                HLT_F = True
            else:
                # print(": ")
                print('HALT NOT PRESENT')
                print(line_counter+1)
                raise NameError("HALT NOT PRESENT")

def acheck(i):
    global line_counter
    if len(i) == 4:
        for j in i[1::]:
            if j == "FLAGS":
                # print(line_counter)
                # print(": ")
                print('FLAG REGISTER CANT BE USED WITH THIS COMMAND')
                print(line_counter+1)
                raise ValueError("FLAG REGISTER CANT BE USED WITH THIS COMMAND")
            if not(j in REGISTERS.keys()):
                # print(line_counter)
                # print(": ")
                print('UNKNOWN REGISTER USED')
                print(line_counter+1)
                raise ValueError("UNKNOWN REGISTER USED")
        line_counter = line_counter + 1
        return True 
    # print(line_counter) 
    # print(": ")
    print('SYNTAX NOT FOLLOWED') 
    print(line_counter+1)
    raise TypeError("SYNTAX NOT FOLLOWED")

def bcheck(i):
    global line_counter
    if len(i) == 3:
        if i[1] in REGISTERS.keys():
            if i[1] != "FLAGS":
                if i[2][0] == '$':
                    if '.' not in i[2][1::]:
                        x = int(i[2][1::])
                        if(x <= MAX_NO and x >= MIN_NO):
                            line_counter = line_counter+ 1
                            return True
                        else:
                            # print(line_counter)
                            # print(": ")
                            print('IMMEDIATE VALUE OFF RANGE')
                            print(line_counter+1)
                            raise OverflowError("IMMEDIATE VALUE OFF RANGE")
                    elif '.' in i[2][1::]:
                        x=CSEToDec(decToCSE(i[2][1::]))
                        line_counter+=1
                else:
                    # print(line_counter)
                    # print(": ")
                    print('IMMEDIATE VALUE OFF RANGE')
                    print(line_counter+1)
                    raise SyntaxError("EXPECTED A $ SIGN")
            else:
                # print(line_counter)
                # print(": ")
                print('THIS OPERATION CANT USE FLAG REGISTER')
                print(line_counter+1)
                raise ValueError("THIS OPPERATION CANT USE FLAG REGISTER")
        else:
            # print(line_counter)
            # print(": ")
            print('INVALID REGISTER')
            print(line_counter+1)
            raise ValueError("INVALID REGISTER")
    else:
        # print(line_counter)
        # print(": ")
        print('SYNTAX NOT FOLLOWED')
        print(line_counter+1)
        raise SyntaxError("SYNTAX NOT FOLLOWED")

def ccheck(i):
    global line_counter
    if len(i) == 3:
        for j in i[1::]:
            if j == "FLAGS":
                # print(line_counter)
                # print(": ")
                print('FLAG REGISTER CANT BE USED WITH THIS COMMAND')
                print(line_counter+1)
                raise ValueError("FLAG REGISTER CANT BE USED WITH THIS COMMAND")
            if not(j in REGISTERS.keys()):
                # print(line_counter)
                # print(": ")
                print('UNKNOWN REGISTER USED')
                print(line_counter+1)
                raise ValueError("UNKNOWN REGISTER USED")
        line_counter = line_counter + 1
        return True
    # print(line_counter)
    # print(": ")
    print('SYNTAX NOT FOLLOWED')
    print(line_counter+1)
    raise TypeError("SYNTAX NOT FOLLOWED")

def dcheck(i):
    global line_counter
    if len(i) == 3:
        if i[1] in REGISTERS.keys():
            if i[1] != "FLAGS":
                if i[2] in var.keys():
                    line_counter = line_counter + 1
                    return True
                else:
                    # print(line_counter)
                    # print(": ")
                    print('VARIABLE DOES NOT EXIST')
                    print(line_counter+1)
                    raise NotImplementedError("VARIABLE DOES NOT EXIST")
            else:
                # print(line_counter)
                # print(": ")
                print('THIS OPERATION CANT USE THE FLAG REGISTER')
                print(line_counter+1)
                raise ValueError("THIS OPERRATION CANT USE FLAG REGISTER")
        else:
            # print(line_counter)
            # print(": ")
            print('INVALID REGISTER')
            print(line_counter+1)
            raise ValueError("INVALID REGISTER")
    else:
        # print(line_counter)
        # print(": ")
        print('SYNTAX NOT FOLLOWED')
        print(line_counter+1)
        raise SyntaxError("SYNTAX NOT FOLLOWED")

def echeck(i):
    global line_counter
    if len(i) == 2:
        if i[1] in var:
            line_counter = line_counter + 1
            return True
        elif i[1] in labels:
            line_counter = line_counter + 1
            return True
        else:
            # print(line_counter)
            # print(": ")
            print('MEM LOCATION DOES NOT EXIST')
            print(line_counter+1)
            raise NotImplementedError("MEM LOCATION DOES NOT EXIST")
    else:
        # print(line_counter)
        # print(": ")
        print('SYNTAX NOT FOLLOWED')
        print(line_counter+1)
        raise SyntaxError("SYNTAX NOT FOLLOWED")

def fcheck(i):
    global line_counter
    if len(i) == 1:
        line_counter = line_counter + 1
        return True
    else:
        # print(line_counter)
        # print(": ")
        print('HALT CANT HAVE ARGUMENTS')
        print(line_counter+1)
        raise SyntaxError("HALT CANT HAVE ARGUMENTS")

def gcheck(i):
    global VAR_F
    global line_counter
    if VAR_F:
        if len(i) == 2:
            if(i[1] in var):
                # print(": ")
                print('VAR ALREADY USED')
                print(line_counter+1)
                raise ExecError("VAR ALREADY USED")
            var[i[1]] = len(var)
            return True
        else:
            # print(line_counter)
            # print(": ")
            print('INVALID SYNTAX')
            print(line_counter+1)
            raise SyntaxError("INVALID SYNTAX")
    else:
        # print(line_counter)
        # print(": ")
        print('LABELS CANT HAVE VAR COMMANDS')
        print(line_counter+1)
        raise ExecError("LABELS CANT HAVE VAR COMMANDS")

def xcheck(i):
    global MOV_TYPE
    global line_counter
    if len(i) == 3:
        if i[1] in REGISTERS.keys():
            # if i[1] != "FLAGS":
                if i[2][0] == '$':
                    x = int(i[2][1::])
                    if(x <= MAX_NO and x >= MIN_NO):
                        line_counter = line_counter+ 1
                        MOV_TYPE='i'
                        if i[1]=='FLAGS':
                            MOV_TYPE='r'
                        return True
                    else:
                        # print(line_counter)
                        # print(": ")
                        print('IMMEDIATE VALUE OFF RANGE')
                        print(line_counter+1)
                        raise OverflowError("IMMEDIATE VALUE OFF RANGE")
                elif i[2] in REGISTERS:
                    line_counter = line_counter+ 1                    
                    MOV_TYPE='r'
                    return True
                else:
                    # print(line_counter)
                    # print(": ")
                    print('INVALID PARAMETER')
                    print(line_counter+1)
                    raise SyntaxError("INVALID PARAMETER")
            # else:
                print(line_counter)
                print(": ")
            #     print('THIS OPERATION CANT USE FLAG REGISTER')
            #     print(line_counter+1)
            #     raise ValueError("THIS OPPERATION CANT USE FLAG REGISTER")
        else:
            # print(line_counter)
            # print(": ")
            print('INVALID REGISTER')
            print(line_counter+1)
            raise ValueError("INVALID REGISTER")
    else:
        # print(line_counter)
        # print(": ")
        print('SYNTAX NOT FOLLOWED')
        print(line_counter+1)
        raise SyntaxError("SYNTAX NOT FOLLOWED")

SYN_CHECK ={
    "A" : acheck,
    "B" : bcheck,
    "C" : ccheck,
    "D" : dcheck,
    "E" : echeck,
    "F" : fcheck,
    "G" : gcheck,
    "X" : xcheck,
    } 

def hcheck(i):
    # print(i)
    if i[0][-1] == ':':
        if len(i) > 1:
            if i[1] != 'var':
                labels[i[0][:-1:]] = line_counter
                if i[1] in isa_type.keys():
                    SYN_CHECK[isa_type[i[1]]](i[1::])
                else:
                    # print(": ")
                    print('INVALID SYNTAX')
                    print(line_counter+1)
                    raise SyntaxError("INVALID SYNTAX")
            else:
                # print(": ")
                print('LABELS CANT HAVE VAR COMMAND')
                print(line_counter+1)
                raise ExecError("LABELS CANT HAVE VAR COMMAND")
        else:
            # print(": ")
            print('INVALID SYNTAX')
            print(line_counter+1)
            raise SyntaxError("INVALID SYNTAX")
    else:
        # print(": ")
        print('INVALID SYNTAX')
        print(line_counter+1)
        raise SyntaxError("INVALID SYNTAX")
     
def syntax_check(p_code):
    initial_check(p_code)
    global VAR_F 
    global HLT_F
    global MEM_F
    
    VAR_F = True
    HLT_F = False
    MEM_F = False
    for i in p_code:
        if i[0] in isa_type.keys():
            SYN_CHECK[isa_type[i[0]]](i)
        else:
            hcheck(i)

# f.close()
# syntax_check(parsed_code)
# print(parsed_code)

def aprint(i):
    res=[]
    res.extend(isa_commands[i[0]])
    res.extend('00')
    res.extend(REGISTERS[i[1]])
    res.extend(REGISTERS[i[2]])
    res.extend(REGISTERS[i[3]])
    return res

def bprint(i):
    res=[]
    res.extend(isa_commands[i[0]])
    res.extend(REGISTERS[i[1]])
    if '.' not in i[2]:
        res.extend(f'{int(i[2]):08b}')
    elif '.' in i[2]:
        res.extend((decToCSE(i[2][1::])[-8::]))
    return res

def cprint(i):
    res=[]
    res.extend(isa_commands[i[0]])
    res.extend('00000')
    res.extend(REGISTERS[i[1]])
    res.extend(REGISTERS[i[2]])
    return res

def dprint(i):
    res=[]
    res.extend(isa_commands[i[0]])
    # res.extend(REGISTERS[i[1][1::]])
    res.extend(REGISTERS[i[1]])
    tempBin=line_counter + var[i[2]]
    res.extend(f'{tempBin:08b}')
    #add line to print memory address of variables as well
    return res

def eprint(i):
    res=[]
    res.extend(isa_commands[i[0]])
    res.extend('000')
    #### IMPORTANT: labels pe hi jump posible he bro variable bas 'ld' 'st' ke liye istemall hone he
    tempBin=labels[i[1]]
    res.extend(f'{tempBin:08b}')
    #add line to print memory address of variables as well
    return res

def fprint(i):
    res=[]
    res.extend(isa_commands[i[0]])
    res.extend('00000000000')
    return res

def gprint(i):
    # res=[]
    # res.extend(isa_commands[i[0]])
    pass

def xprint(i):
    global MOV_TYPE
    res=[]
    if i[1]=='FLAGS' or i[2]=='FLAGS':
        res.extend(isa_commands['movr'])
        res.extend('00000')
        res.extend(REGISTERS[i[1]])
        res.extend(REGISTERS[i[2]])
    else:    
        if MOV_TYPE=='i':
            # res=[]
            res.extend(isa_commands['movi'])
            res.extend(REGISTERS[i[1]])
            temp=int(i[2][1::])
            res.extend(f'{temp:08b}')
            # print(MOV_TYPE)
            # return res
        elif MOV_TYPE=='r':
            # res=[]
            res.extend(isa_commands['movr'])
            res.extend('00000')
            res.extend(REGISTERS[i[1]])
            res.extend(REGISTERS[i[2]])
    return res
# def hprint(i):
#     print_code(i)


SYN_PRINT ={
    "A" : aprint,
    "B" : bprint,
    "C" : cprint,
    "D" : dprint,
    "E" : eprint,
    "F" : fprint,
    "G" : gprint,
    "X" : xprint
} 

def printString(a):
    print(' '.join(a))
    print("\n")

def print_code(parsed_code):
    # counting=0
    with open('printBinary.txt','w') as wTB:
        for instruct in parsed_code:
            if instruct[0] in isa_type.keys():
                printing=SYN_PRINT[isa_type[instruct[0]]](instruct)
                if printing!=None:
                    temp = ''.join([str(elem) for elem in printing])
                    wTB.write(temp)
                    wTB.write('\n')
                    print(temp)
                    # counting+=1
            else:
                printing=SYN_PRINT[isa_type[instruct[1]]](instruct[1::])
                if printing!=None:
                    temp=''.join([str(elem) for elem in printing])
                    wTB.write(temp)
                    wTB.write('\n')
                    print(temp)
                    # counting+=1

# print(parsed_code)
syntax_check(parsed_code)
print_code(parsed_code)
f.close()
