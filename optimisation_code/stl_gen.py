import numpy as np
import stl
import shutil
from stl import mesh

def STL_Gen(x,y,g,s):
    res = len(x)
   # x=[x[i]/1000 for i in range(len(x))]
    #y=[y[i]/1000 for i in range(len(x))]
    z=0.1
    i = 0; v=[]
    while (i <res): # +ve z axis points
        v.append([x[i],y[i],z])
        i += 1
    i=0
    while (i <res): # -ve z axis points
        v.append([x[i],y[i],-z])
        i += 1
    vertices=np.array(v)

    i=0; f=[]
    while (i<res-1): # generating faces
        f.append([i,i+1,res+i+1])
        f.append([i,res+i+1,res+i])
        i +=1
    faces= np.array(f)


    suf=mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            suf.vectors[i][j]= vertices[f[j],:]
    suf.save('Airfoil_%i-%i.stl'%(g,s), mode=stl.Mode.ASCII)
    shutil.copyfile('Airfoil_%i-%i.stl'%(g,s), 'constant/triSurface/Airfoil1.stl')
    
