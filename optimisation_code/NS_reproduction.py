from constants import Cmax, Cmin, nPop
from airfoil_Class import airfoil #baby_airfoil
import random
import copy
from NSGA2 import *

def Rank_Assign(Airfoil, Cost0, Cost1):

    #Cost=Airfoil[0].Lists(Airfoil,1)
    NDSa=fast_non_dominated_sort(Cost0,Cost1)
    #print(NDSa)
    CDv=[]
    for i in range(0,len(NDSa)):
    	CDv.append(crowding_distance(Cost0,Cost1,NDSa[i][:]))
    Rank_List=[]
    for i in range(0,len(NDSa)):
        NDSa2 = [index_of(NDSa[i][j],NDSa[i] ) for j in range(0,len(NDSa[i]))]
        front22 = sort_by_values(NDSa2[:], CDv[i][:])
        front = [NDSa[i][front22[j]] for j in range(0,len(NDSa[i]))]
        front.reverse()
        #print(front)
        for value in front:
    	    Rank_List.append(value)
    	    if(len(Rank_List)==len(Airfoil)):
    	    	break
        if (len(Rank_List) == len(Airfoil)):
    	    break
    #Sorted_Airfoil = []
    for i in range(len(Airfoil)):
    	Airfoil[Rank_List[i]].rank = i
        #Sorted_Airfoil.append(Airfoil[Rank_List[i]])

    return NDSa

def reproduction(Airfoil, gen, sigma, x, s, r, l):  
                     
    costs = []
    ranks = []
    
    for t in range(len(Airfoil)):
        costs.append(Airfoil[t].cost)
        ranks.append(Airfoil[t].rank)

    #BestCost = max(costs)
    WorstRank = max(ranks)

    #WorstCost = min(costs)
    #j = 0
    #while 1:
    #    if r[j] > nPop:
    #        break

    #    if r[j] <= nPop:
    #        j+=1
    #    
    #    elif j>l:
    #        break

    j = l/4

    i = 0 

    while 1:
        if x < r[i]:
            break            

        if x >= r[i]:
            i +=1

        elif i > l:
            break

    #ratio = ((j-i)/j)**2
    ratio = (WorstRank - Airfoil[x].rank)/(WorstRank)
    C = int(Cmin + (Cmax - Cmin)*ratio)
    #print(Airfoil[x].rank)
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
            #progeny[j].mean_camber(gen, s[0])
            progeny[j].camber(gen, s[0])
	    
            #add camber calc function here
            
            #progeny[j].mutate(sigma)
                                 
            s[0] += 1

        for j in range(C):

            progeny[j].xFoil()
            #progeny[j].camber(gen, s[0])
            #progeny[j].mean_camber(gen, s[0])
            #print(progeny[j].cost)
            #progeny[j].cfd()
            Airfoil.append(progeny[j])
