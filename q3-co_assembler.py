# def convertToFP(a):
    
    
#     pass

# isa_commands={}

# fp_commands={
#     "f_add":"00000",
#     "f_sub":"00001",
#     "f_mov":"00010"
# }

# isa_commands.extend(fp_commands)

# isa_type={}

# fp_type={
#     "f_add":"A",
#     "f_sub":"A",
#     "f_mov":"B"    
# }

# isa_type.extend(fp_type)

num="4.53"
num_list=num.split(".")
# for i in range(len(num_list)): 
#     num_list[i]=int(num_list[i])
print(num_list)

first=format(int(num_list[0]),"b")

second=''
num_list[1]=int(num_list[1])
while len(second)<5:
    num_list[1]*=2
    if num_list[1]>10:
        num_list[1]-=10
        second+="1"
    elif num_list[1]<10:
        second+="0"
    elif num_list[1]==10:
        second+="1"
print(second)

print(f'{first}.{second}')
exponent=len(first)-1
if exponent>3:
    print("overflow")
binary=f'{first[1::]}{second}'
print(bin(exponent)[2::])
print(binary)
cse_rep=f'{bin(exponent)[2:5:]}{binary[:5]}'
print(cse_rep)

