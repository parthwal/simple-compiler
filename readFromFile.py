def read():
    inp=[""]
    ins=[]
    with open("instructions.txt",'r') as rFF:
        while inp!=["hlt"]:
            inp=rFF.readline().split()
            # print(inp)
            ins.append(inp)
        return ins
# print(read())