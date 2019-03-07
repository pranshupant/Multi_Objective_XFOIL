from constants import maxIt, Gen0, sigma_final, sigma_initial, exponent, nPop
from airfoil_Class import airfoil, baby_airfoil
import subprocess as sp
import os
import numpy as np
from reproduction import reproduction
from multiprocessing import Pool
import time as t

Airfoil = []
st = [0]
s = np.array(st)
Result = []

for i in range(Gen0):

    Airfoil.append(airfoil(0,i))
    Airfoil[i].ctrlPoints()
    Airfoil[i].bspline()
    Airfoil[i].write()
    Airfoil[i].savefig()

#for i in range(Gen0):
def firstGen_cost(i):
    #Airfoil[i].savefig()
    Airfoil[i].xFoil()
    #Airfoil[i].cfd()
    print(Airfoil[i].cost)
    return Airfoil[i].cost

p = Pool()

pResult = p.map(firstGen_cost, range(Gen0))
p.close()
p.join()

for i in range(Gen0):
    Airfoil[i].cost = pResult[i]

#print(len(Result))
#t.sleep(25)
gen = 1

if __name__ == "__main__":

    while gen < maxIt:

        sigma = (((maxIt - float(gen-1))/maxIt)**exponent)*(sigma_initial - sigma_final) + sigma_final

        Airfoil.sort(key = lambda x: x.cost, reverse = True)

        for i in range(len(Airfoil)):
            print(Airfoil[i].cost)

        del Airfoil[nPop:]

        for i in range(len(Airfoil)):
            print(Airfoil[i].cost)

        parent = []
    
        for k in range(nPop):
            parent.append(baby_airfoil(Airfoil[k], gen, s[0]))
            parent[k].write()

            s[0] += 1 

        for k in range(nPop):
        
            parent[k].xFoil()
            #parent[k].cfd()
            parent[k].savefig()

        '''def carryGen_cost(i):
            #Airfoil[i].savefig()
            parent[i].xFoil()
            parent[i].savefig()
            #parent[i].cfd()
            return parent[i].cost
        
        r = Pool()
        rResult = r.map(carryGen_cost, range(nPop))
        r.close()
        r.join()

        for j in range(nPop):
            parent[j].cost = pResult[j]'''

        #def other_Gens(x):
        #    reproduction(Airfoil, gen, sigma, x, s)

        for x in range(len(Airfoil)):
        
        #q = Pool(2)
        #q.map(other_Gens, range(len(Airfoil)))
        #q.close()
        #q.join()
            
            reproduction(Airfoil, gen, sigma, x, s)      

        gen += 1 
        s[0] = 0      