import math

mem=input("The space in memory: ")
addr=input("The memory address type (1/2/3/4): ")
d={"kB":2**13,"MB":2**23,"GB":2**33,"kb":2**10,"Mb":2**20,"Gb":2**30}


def typeB1():
    global addr
    bits_cpu=input("How many bits is the CPU: ")
    addr_change=input("Enhanced addressable memory type (1/2/3/4): ")
    
    d2={"1":1,"2":4,"3":8,"4":bits_cpu}
    max_mem= d[mem[-2::]] * int(mem.split()[0])
    net_pins=int(math.log(max_mem/int(d2[addr_change]),2) - math.log(max_mem/int(d2[addr]),2))
    
    print(f"Pins saved: {net_pins}")
    
def typeB2():
    cpu_bits=int(input("How many bits is the CPU: "))
    cpu_pins=int(input("How many Address Pins in the CPU: "))
    cpu_addr=input("The memory address type (1/2/3/4): ")
    
    cpu_bytes=cpu_bits//8
    if(cpu_addr!="4"):
        if(cpu_pins>30):
            print("Maximum size of main memory: ",2**(cpu_pins-30),"GB")
        elif(cpu_pins>20 and cpu_pins<=30):
            print("Maximum size of main memory: ",2**(cpu_pins-20),"MB")
        elif(cpu_pins>10 and cpu_pins<=20):
            print("Maximum size of main memory: ",2**(cpu_pins-10),"KB")
        elif(cpu_pins>0 and cpu_pins<=10):
            print("Maximum size of main memory: ",2**(cpu_pins-0),"B")
        else:
            print("Maximum size of main memory: Zero Memory")

    else:
        if(cpu_pins>30):
            print("Maximum size of main memory: ",cpu_bytes*2**(cpu_pins-30),"GB")
        elif(cpu_pins>20 and cpu_pins<=30):
            print("Maximum size of main memory: ",cpu_bytes*2**(cpu_pins-20),"MB")
        elif(cpu_pins>10 and cpu_pins<=20):
            print("Maximum size of main memory: ",cpu_bytes*2**(cpu_pins-10),"KB")
        elif(cpu_pins>0 and cpu_pins<=10):
            print("Maximum size of main memory: ",cpu_bytes*2**(cpu_pins-0),"B")
        else:
            print("Maximum size of main memory: Zero Memory")


def typeA1():
    global d
    global d2
    len_ins=int(input("What is the length of one instruction (in bits): "))
    len_reg=int(input("What is the length of one register (in bits): "))
    
    max_ins=int(math.log(len_ins*d[mem[-2::]]*int(mem.split()[0])))
    if (max_ins<=len_reg):
        print("ERROR: Register is not supported")
        exit()
    elif(max_ins-len_reg>=6):
        op_bits=5
    elif(max_ins-len_reg>=4 and max_ins-len_reg<=5):
        op_bits=3
    
    print(f"Minimum bits required to represent an address: {max_ins}")
    print(f"Bits needed by opcode: {op_bits}")
    print(f"P-bit Address bits in Instruction Type A1: {max_ins-len_reg-op_bits}")
    print(f"Register Address Bits: {len_reg}")
    print(f"Maximum number of supported instructions for given ISA: {2**op_bits}")
    print(f"Maximum number of supported registers for given ISA: {2**len_reg}")

def typeA2():
    global d
    global d2
    len_ins=int(input("What is the length of one instruction (in bits): "))
    len_reg=int(input("What is the length of one register (in bits): "))
    
    max_ins=int(math.log(len_ins*d[mem[-2::]]*int(mem.split()[0])))
    if (max_ins<=2*len_reg):
        print("ERROR: Register is not supported")
        exit()
    elif(max_ins-2*len_reg>=6):
        op_bits=5
    elif(max_ins-2*len_reg>=4 and max_ins-2*len_reg<=5):
        op_bits=3
    
    print(f"Minimum bits required to represent an address: {max_ins}")
    print(f"Bits needed by opcode: {op_bits}")
    print(f"R-Filler bits in Instruction Type A2: {max_ins-2*len_reg-op_bits}")
    print(f"Register Address Bits: {2*len_reg}")
    print(f"Maximum number of supported instructions for given ISA: {2**op_bits}")
    print(f"Maximum number of supported registers for given ISA: {2**len_reg}")


def typeA():
    query=input("Input Type (1/2): ")
    if query=="1":
        typeA1()
    elif query=="2":
        typeA2()
    else:
        print("Not an option, try again")
        typeA()

def typeB():
    query=input("Input Type (1/2): ")
    if query=="1":
        typeB1()
    elif query=="2":
        typeB2()
    else:
        print("Not an option, try again")
        typeB()

#driver
query=input("Input Query (1/2): ")
if query=='1':
    typeA()
elif query=='2':
    typeB()
else:
    print("----Exiting----")
    exit()
