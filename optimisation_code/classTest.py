from airfoil_Class import airfoil
import subprocess as sp
import os

g = 5
s = 10
Airfoil = []

for i in range(g):
    for j in range(s): 
        Airfoil.append(airfoil(i,j))

for i in range(50):
    
    Airfoil[i].bspline()
    Airfoil[i].write()
    #Airfoil[i].savefig()
    
for i in range(50): 
    Airfoil[i].cfd()
    print(Airfoil[i].cost)
    #Airfoil[i].cfd()

'''for i in range(5):
    print(Airfoil[i].number)
    print(Airfoil[i].cost)
    Airfoil[i].show()
'''

'''os.chdir("/home/pranshu/Desktop/openFoam/2D_SImpleFoamWing_1")
print(os.getcwd())
sp.call(['./Allclean'])
sp.call(['./Allrun.sh'])
'''
