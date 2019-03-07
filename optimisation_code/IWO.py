from constants import maxIt, Gen0, sigma_final, sigma_initial, exponent, nPop
from airfoil_Class import airfoil#, baby_airfoil
import subprocess as sp
import os
import numpy as np
from reproduction import reproduction
from multiprocessing import pool

Airfoil = []
st = [0]
s = np.array(st)
gen = 0


for i in range(Gen0):
    
    Airfoil.append(airfoil(0,i))
    Airfoil[i].ctrlPoints()
    Airfoil[i].bspline()
    Airfoil[i].write()
    Airfoil[i].savefig()
    Airfoil[i].show(gen, i)
    Airfoil[i].camber(gen, i)


for i in range(Gen0):
    #Airfoil[i].savefig()
    #Airfoil[i].xFoil()
    Airfoil[i].cfd()
    print(Airfoil[i].cost)

gen = 1

if __name__ == "__main__":

    while gen < maxIt:

        sigma = (((maxIt - float(gen-1))/maxIt)**exponent)*(sigma_initial - sigma_final) + sigma_final

        print('SIGMA')
        print(sigma)
        
        Airfoil.sort(key = lambda Airfoil: Airfoil.cost, reverse = True)

        for i in range(len(Airfoil)):
            print(Airfoil[i].cost)

        del Airfoil[nPop:]
               

        for i in range(len(Airfoil)):
            print(Airfoil[i].cost)
    
        for k in range(nPop):
            Airfoil[k].copy(gen, s[0])
            Airfoil[k].copy_Results(gen, s[0])
            Airfoil[k].show(gen, s[0])
            Airfoil[k].camber(gen, s[0])
            s[0] += 1 


        for x in range(len(Airfoil)):
            reproduction(Airfoil, gen, sigma, x, s)    

        Airfoil.sort(key = lambda x: x.cost, reverse = True)
                
        gen += 1 
        s[0] = 0      