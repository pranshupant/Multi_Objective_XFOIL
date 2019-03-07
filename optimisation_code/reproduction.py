from constants import Cmax, Cmin, nPop
from airfoil_Class import airfoil #baby_airfoil
import random
import copy

def reproduction(Airfoil, gen, sigma, x, s):  
                     
    costs = []
    
    for t in range(len(Airfoil)):
        costs.append(Airfoil[t].cost)

    BestCost = max(costs)

    WorstCost = min(costs)

    ratio = (Airfoil[x].cost - WorstCost)/(BestCost - WorstCost)
    C = int(Cmin + (Cmax - Cmin)*ratio)
    print(Airfoil[x].cost)
    print(C)

    if C > 0:

        progeny = []
       
        for j in range(C):
            
            p = copy.deepcopy(Airfoil[x])
            p.copy_mutate(gen, s[0])
            progeny.append(p)

            progeny[j].new(sigma)
            progeny[j].bspline()
            progeny[j].write()
            progeny[j].savefig()
            progeny[j].show(gen, s[0])
            progeny[j].camber(gen, s[0])

                                 
            s[0] += 1

        for j in range(C):

            #progeny[j].xFoil()
            #progeny[j].cfd()
            progeny[j].error('s1223.dat')
            print(progeny[j].cost)
            Airfoil.append(progeny[j])