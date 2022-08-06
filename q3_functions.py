inp="193.2"
def decToCSE(inp):
    print(inp)
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
    mantissa=f'{first[1::]}{second}'
    # print(mantissa)
    if len(mantissa)>5:
        print("Mantissa longer than 5, Truncating till 5 digits")
    mantissa=mantissa[:5:]
    # print(mantissa)
    exponent=len(str(first))
    # print(exponent)
    if exponent>7:
        print("Overflow: Exponent Greater than 7")
    exponent=bin(exponent-1).replace('0b','')
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
    print(cse_rep)
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
    print(out)
    return(out)

# decToCSE(inp)
CSEToDec(decToCSE(inp))
