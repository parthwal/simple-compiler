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

print(decitobin(10),bintodeci("1010"),bool("1"),bool(int("0")),int(True),int(False))