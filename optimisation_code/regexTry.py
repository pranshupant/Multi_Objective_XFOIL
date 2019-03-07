import re


f = open("Results_XFoil/Generation_0/Specie_0/solution.txt", "r")
for line in f:
    line = f.read()

    #print(line)
    #row = line.split()
    
    p = re.findall('\s+[.\d]{5}\s+([.\d]{6})\s+([.\d]{7})\s+', line)
    #print(row)
#print(line)


#p = re.findall('25\s+([-.A-Za-z0-9]+)\s+([-.A-Za-z0-9]+)', line)

#p = re.findall('^\s+[.\d]{5}\s+([.\d]{6})\s+([.\d]{6})', line)

print(float(p[0][0])/float(p[0][1]))
z = line
#print(z)
f.close()