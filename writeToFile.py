def input(): #input instructions
    val=""
    with open("instructions.txt","w") as wTF:
        while(val.lower()!="hlt"):
            val=input().lower()
            wTF.write(val)
            wTF.write("\n")