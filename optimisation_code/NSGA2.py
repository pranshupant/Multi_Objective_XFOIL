import csv, random, re, sys, os, math, numpy as np, time, subprocess, shutil
import matplotlib.pyplot as plt 
from multiprocessing import Pool
from distutils.dir_util import copy_tree
import scipy.interpolate as si


def index_of(a,list):
    for i in range(len(list)):
        if list[i] == a:
            return i
    return -1

def sort_by_values(l, V):
    SL = []
    while(len(SL)!=len(l)):
        if index_of(min(V),V) in l:
            SL.append(index_of(min(V),V))
        V[index_of(min(V),V)] = math.inf
    return SL

def fast_non_dominated_sort(V1, V2):
    S=[[] for i in range(0,len(V1))]
    F = [[]]
    n=[0 for i in range(0,len(V1))]
    rank = [0 for i in range(0, len(V1))]

    for p in range(0,len(V1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(V1)):
            if (V1[p] > V1[q] and V2[p] > V2[q]) or (V1[p] >= V1[q] and V2[p] > V2[q]) or (V1[p] > V1[q] and V2[p] >= V2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (V1[q] > V1[p] and V2[q] > V2[p]) or (V1[q] >= V1[p] and V2[q] > V2[p]) or (V1[q] > V1[p] and V2[q] >= V2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in F[0]:
                F[0].append(p)

    i = 0
    while(F[i] != []):
        Q=[]
        for p in F[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        F.append(Q)

    del F[len(F)-1]
    
    return F

def crowding_distance(V1, V2, F):
    D = [0 for i in range(0,len(F))]
    sorted1 = sort_by_values(F, V1[:])
    sorted2 = sort_by_values(F, V2[:])
    D[0] = 2**100#math.inf
    D[len(F) - 1] = 2**100 #math.inf
    for k in range(1,len(F)-1):
        D[k] = D[k]+ (V1[sorted1[k+1]] - V2[sorted1[k-1]])/(max(V1)-min(V1))
    for k in range(1,len(F)-1):
        D[k] = D[k]+ (V1[sorted2[k+1]] - V2[sorted2[k-1]])/(max(V2)-min(V2))
    return D
