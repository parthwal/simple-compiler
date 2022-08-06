import matplotlib.pyplot as plt

# q4 utilities
'''
time = 0
after every exec time increments such as after retriving mem executing etc (exeption dumping and upgrading pc)

'''
mem_adress = []
f = open("mem.txt")
pcode = f.read().strip().split("\n")
p_code = [i.split() for i in pcode]
x = []
y = []
for i in p_code:
    x.append(i[0])
    y.append(i[1])

plt.scatter(x, y)
plt.show()

