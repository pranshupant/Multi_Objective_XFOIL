import numpy as np
from scipy import interpolate
from constants import *
import matplotlib.pyplot as plt
import random
import stl
from stl import mesh
from stl_gen import STL_Gen
import subprocess as sp
import shutil
from shutil import copyfile, copytree
import sys
import string
import re
import os
import time
import copy

class airfoil:
    def __init__(self, gen, spec):
        
        self.__generation = gen
        self.__specie = spec
        self.__uPoint = np.zeros((6,2))
        self.__lPoint = np.zeros((6,2))
        self.plotX = []
        self.plotY = []
        self.c_Lower = np.zeros(100)
        self.c_Upper = np.zeros(100)   
        self.c_X = np.zeros(100) 
        self.cost = -10.00
        self.rank = 0.00
        self.max_Camber = 25.00

    def ctrlPoints(self): #Import bspline.py

        LBY = 0.05 # Upper Array
        UBY = 0.3

        LBY2 = -0.1 # Lower Array
        UBY2 = 0.1

        LBX = 0.05
        UBX = 0.85

        
        self.__uPoint[1] = [0, random.uniform(-0.1, -0.025)] # Lower Array
        self.__uPoint[5] = [1, 0]

        for i in range(2, 5):
            self.__uPoint[i][0] = random.uniform((LBX if (i==2) else self.__uPoint[i-1][0]+0.05),
                                         (0.2*i if not (i==4) else UBX))
            self.__uPoint[i][1] = random.uniform(LBY2, UBY2)

        self.__lPoint[1] = [0, random.uniform(0.05, 0.15)] # Upper Array
        self.__lPoint[5] = [1, 0]

        for i in range(2, 5):
            self.__lPoint[i][0] = random.uniform((LBX if (i==2) else self.__lPoint[i-1][0]+0.05),
                                         (0.2*i if not (i==4) else UBX))
            self.__lPoint[i][1] = random.uniform(LBY if (LBY>self.__uPoint[i][1]) 
                                             else self.__uPoint[i][1]+0.03, UBY)

        #print(self.__uPoint)
        #print(self.__lPoint)
    def bspline(self):
        # Split into new function
        ctr = np.array(self.__lPoint)
        ltr = np.array(self.__uPoint)

        x = ctr[:,0]
        y = ctr[:,1]

        x1 = ltr[:,0]
        y1 = ltr[:,1]


        l=len(x)
        t=np.linspace(0,1,l-2,endpoint=True)
        t=np.append([0,0,0],t)
        t=np.append(t,[1,1,1])

        tck=[t,[x,y],3]
        lck=[t,[x1,y1],3]
        u3=np.linspace(0,1,(max(l*2,100)),endpoint=True)
        out = interpolate.splev(u3,tck) 
        out1 = interpolate.splev(u3,lck) 
        
        X1=np.array(out[0])
        c_X = copy.deepcopy(X1)
        self.c_X = c_X[0:100]

        X2=np.array(out1[0])
        X3=X1[: : -1]

        X=np.concatenate((X3,X2), 0)
        self.plotX = X     

        Y1=np.array(out[1])
        cY1 = copy.deepcopy(Y1)
        self.c_Upper = cY1[0:100]


        Y2=np.array(out1[1])
        cY2 = copy.deepcopy(Y2)
        self.c_Lower = cY2[0:100]


        Y3=Y1[: : -1]

        Y=np.concatenate((Y3,Y2), 0)
        self.plotY = Y

        #STL_Gen(X,Y,g,s)
        #print("Airfoil created")


    def write(self):

        #print(self.__generation)
        #print(self.__specie)

        if(not os.path.isdir("Results_XFoil/Generation_%i/Specie_%i" %(self.__generation,self.__specie))):
            os.makedirs("Results_XFoil/Generation_%i/Specie_%i" %(self.__generation,self.__specie))
            
        f = open("Results_XFoil/Generation_%i/Specie_%i/plot_Airfoil_%i-%i" %(self.__generation,self.__specie,self.__generation,self.__specie),"w+")

        f.write("Airfoil_%i-%i"%(self.__generation,self.__specie))
        f.write("\n")

        for i in range(len(self.plotX)):
            f.write(str(self.plotX[i]))
            f.write(" ")
            f.write(str(self.plotY[i]))
            f.write("\n")
        f.close()

        f = open("Results_XFoil/Generation_%i/Specie_%i/Genes_Airfoil_%i-%i" %(self.__generation,self.__specie,self.__generation,self.__specie),"w+")

        for i in range(5):
            f.write(str(self.__uPoint[i]).strip('[]'))
            f.write('\n')
        for i in range(5):
            f.write(str(self.__lPoint[i]).strip('[]'))
            f.write('\n')
        f.close()

        '''if(not os.path.isdir("Results_CFD/Generation_%i/Specie_%i" %(self.__generation,self.__specie))):
            os.makedirs("Results_CFD/Generation_%i/Specie_%i" %(self.__generation,self.__specie))

        f = open('Results_CFD/Generation_%i/Specie_%i/plot_Airfoil_%i-%i'%(self.__generation,self.__specie,self.__generation,self.__specie),"w+")

        f.write("Airfoil_%i-%i"%(self.__generation,self.__specie))
        f.write("\n")

        for i in range(len(self.plotX)):
            f.write(str(self.plotX[i]))
            f.write(' ')
            f.write(str(self.plotY[i]))
            f.write('\n')
        f.close()

        f = open('Results_CFD/Generation_%i/Specie_%i/Genes_Airfoil_%i-%i'%(self.__generation,self.__specie,self.__generation,self.__specie),"w+")

        for i in range(5):
            f.write(str(self.__uPoint[i]).strip('[]'))
            f.write('\n')
        for i in range(5):
            f.write(str(self.__lPoint[i]).strip('[]'))
            f.write('\n')
        f.close()'''
              

    def xFoil(self): 
        
        #Extraction of L/d done
        os.chdir('Results_XFoil/Generation_%i/Specie_%i'%(self.__generation,self.__specie))
        #print(os.getcwd())

        copyfile("plot_Airfoil_%i-%i" %(self.__generation,self.__specie), "Airfoil.txt")
        copyfile("../../../controlfile.xfoil", "controlfile.xfoil")

        #t1 = time.time()

        sp.Popen(['xfoil <controlfile.xfoil>outputfile.out'],
         stdin=sp.PIPE,
         stdout=None,
         stderr=None,
         shell=True
         )

        p = []

        t1 = time.time()

        t2 = 0

        while t2 < 2:

            t2 = time.time() - t1

            if os.path.isfile('plot.ps'):
                
                if os.path.isfile("solution.txt"):        
                    f = open("solution.txt", "r+")
                    for line in f:
                        line = f.read()      
                    p = re.findall(r'\s+[.\d]{5}\s+(-?[.\d]{6})\s+(-?[.\d]{7})', line) 
                break

            else:

                p.append([-10.00,1.00])
                # print("File not found")
                #self.max_Camber = 25.00
          

        if not p:

            r = -10.00
            self.cost = r
            #self.max_Camber = 25.00

        elif p:
            
            r = float(p[0][0])/float(p[0][1])
            self.cost = r 
            #self.max_Camber = float(p[0][1])

        os.chdir('../../../../optimisation_code')
        

    def cfd(self):  #Extract result from post processing

        os.chdir('Results_CFD/Generation_%i/Specie_%i'%(self.__generation,self.__specie))
        #os.mkdir('CFD')

        copytree('../../../IWO_CFD_orig', 'CFD')
               
        os.chdir('CFD')

        STL_Gen(self.plotX,self.plotY,self.__generation,self.__specie)


        print(os.getcwd())
        sp.call(['./Allclean'])
        sp.call(['./Allrun.sh'])

        if os.path.isfile('postProcessing/forceCoeffs1/0/forceCoeffs.dat'):

            f = open("postProcessing/forceCoeffs1/0/forceCoeffs.dat", "r")
            for line in f:
                 line = f.read()

            #p = re.findall(r'2000\s+([-.A-Za-z0-9]+)\s+([-.A-Za-z0-9]+)', line)
            p = re.findall(r'2500\s+(-?\d\.\d{6})e([-+\d]{3})\s+(-?\d\.\d{6})e([-+\d]{3})\s+(-?\d\.\d{6})e([-+\d]{3})', line)

            try:
                
                r = float(p[0][4])*(10.0**int(p[0][5]))/(float(p[0][2])*(10.0**int(p[0][3])))
                self.cost = r

            except IndexError:

                self.cost = -11

            except ValueError:
                self.cost = -9

        else:

            self.cost = -10

        os.chdir('../../../../../optimisation_code')


    def copy(self, g, s):
        
        if(not os.path.isdir("Results_XFoil/Generation_%i/Specie_%i" %(g,s))):
            os.makedirs("Results_XFoil/Generation_%i/Specie_%i" %(g,s))
            
        f = open("Results_XFoil/Generation_%i/Specie_%i/plot_Airfoil_%i-%i" %(g,s,g,s),"w+")

        f.write("Airfoil_%i-%i"%(g,s))
        f.write("\n")

        for i in range(len(self.plotX)):
            f.write(str(self.plotX[i]))
            f.write(" ")
            f.write(str(self.plotY[i]))
            f.write("\n")
        f.close()

        f = open("Results_XFoil/Generation_%i/Specie_%i/Genes_Airfoil_%i-%i" %(g,s,g,s),"w+")

        for i in range(5):
            f.write(str(self.__uPoint[i]).strip('[]'))
            f.write('\n')
        for i in range(5):
            f.write(str(self.__lPoint[i]).strip('[]'))
            f.write('\n')
        f.close()

        '''if(not os.path.isdir("Results_CFD/Generation_%i/Specie_%i" %(g,s))):
            os.makedirs("Results_CFD/Generation_%i/Specie_%i" %(g,s))

        f = open('Results_CFD/Generation_%i/Specie_%i/plot_Airfoil_%i-%i'%(g,s,g,s),"w+")

        f.write("Airfoil_%i-%i"%(g,s))
        f.write("\n")

        for i in range(len(self.plotX)):
            f.write(str(self.plotX[i]))
            f.write(' ')
            f.write(str(self.plotY[i]))
            f.write('\n')
        f.close()

        f = open('Results_CFD/Generation_%i/Specie_%i/Genes_Airfoil_%i-%i'%(g,s,g,s),"w+")

        for i in range(5):
            f.write(str(self.__uPoint[i]).strip('[]'))
            f.write('\n')
        for i in range(5):
            f.write(str(self.__lPoint[i]).strip('[]'))
            f.write('\n')
        f.close()'''

        # Write code for copying airfoil solution data from previous __generation to new __generation
    def copy_Results(self, g, s):
        
        #os.chdir()
        try:
            copyfile('Results_XFoil/Generation_%i/Specie_%i/plot.ps'%(self.__generation, self.__specie), 'Results_XFoil/Generation_%i/Specie_%i/plot.ps'%(g, s))
            
        except FileNotFoundError:
            print('XFoil_plot---File to be copied is missing')
        
        try:
            copyfile('Results_XFoil/Generation_%i/Specie_%i/solution.txt'%(self.__generation, self.__specie), 'Results_XFoil/Generation_%i/Specie_%i/solution_copy.txt'%(g, s))

        except FileNotFoundError:
            print('XFoil_solution---File to be copied is missing')

        '''try:
            copytree('Results_CFD/Generation_%i/Specie_%i/CFD'%(self.__generation, self.__specie), 'Results_CFD/Generation_%i/Specie_%i/CFD'%(g, s) )

        except FileNotFoundError:
            print('CFD Folder missing...')

        try:
            copyfile('error/%i--%i.svg'%(self.__generation, self.__specie), 'error/%i--%i.svg'%(g, s))
            
        except FileNotFoundError:
            print('Error_plot---File to be copied is missing')'''



    def show(self, g, s):   #display using matplotlib

        plt.plot(self.__uPoint[:,0], self.__uPoint[:,1],'k--',label='Control polygon',marker='o',markerfacecolor='red')
       
        plt.plot(self.__lPoint[:,0],self.__lPoint[:,1],'k--',label='Control polygon',marker='o',markerfacecolor='green')
       
        plt.plot(self.plotX, self.plotY,'b',linewidth=2.0,label='B-spline curve')
        
        plt.legend(loc='best')
        plt.axis([0, 1, -0.25, 0.5])
        plt.axis('equal')
        plt.title('Cubic B-spline curve evaluation%i--%i'%(self.__generation, self.__specie))
        plt.savefig(plotsDirectory%(g,s))
        plt.savefig(xFoil_image%(g, s, g, s), bbox_inches = 'tight')

        #plt.show()
        plt.close()

    def savefig(self):   #display using matplotlib

        plt.plot(self.__uPoint[:,0], self.__uPoint[:,1],'k--',label='Control polygon',marker='o',markerfacecolor='red')
       
        plt.plot(self.__lPoint[:,0],self.__lPoint[:,1],'k--',label='Control polygon',marker='o',markerfacecolor='green')
       
        plt.plot(self.plotX, self.plotY,'b',linewidth=2.0,label='B-spline curve')
        
        plt.legend(loc='best')
        plt.axis([0, 1, -0.25, 0.5])
        plt.axis('equal')
        plt.title('Cubic B-spline curve evaluation')
        #plt.savefig('/home/pranshu/Documents/Visual_Studio_Code/optimisation_code/Results_CFD/Generation_%i/Specie_%i/airfoil_%i-%i.png'%(self.__generation,self.__specie,self.__generation,self.__specie), bbox_inches = "tight")
        #copyfile('airfoil_%i-%i.png', '/home/pranshu/Documents/Visual_Studio_Code/optimisation_code/Results_XFoil/Generation_%i/Specie_%i/airfoil_%i-%i.png'%(self.__generation,self.__specie,self.__generation,self.__specie))
        plt.savefig(xFoil_image%(self.__generation,self.__specie,self.__generation,self.__specie), bbox_inches = 'tight')
        plt.close()

#class baby_airfoil(airfoil):

    def copy_mutate(self, g, s):

        self.__generation = g
        self.__specie = s

    def new(self, sigma):

        #print("MUTATION")
        #print('%i-%i'%(self.__generation, self.__specie))
    
        LBY = 0.05 # Upper Array
        UBY = 0.3

        LBY2 = -0.1 # Lower Array
        UBY2 = 0.10

        LBX = 0.025
        UBX = 0.85

        self.__uPoint[1][1] = self.__uPoint[1][1] + M*sigma*random.uniform(-1,1)   
        self.__uPoint[1][1] = max(self.__uPoint[1][1], -0.1)
        self.__uPoint[1][1] = min(self.__uPoint[1][1], -0.025)

        self.__lPoint[1][1] = self.__lPoint[1][1] + M*sigma*random.uniform(-1,1)   
        self.__lPoint[1][1] = min(self.__lPoint[1][1], 0.15)
        self.__lPoint[1][1] = max(self.__lPoint[1][1], 0.05)


        for i in range(2,5):
            self.__uPoint[i][0] = self.__uPoint[i][0] + M*sigma*random.uniform(-1,1)
                
      
            self.__uPoint[i][0] = min(self.__uPoint[i][0], UBX)
            self.__uPoint[i][0] = max(self.__uPoint[i][0], self.__uPoint[i-1][0]+0.05)
            self.__uPoint[i][0] = min(self.__uPoint[i][0], UBX)

            

        for i in range(2,5):
            self.__lPoint[i][0] = self.__lPoint[i][0] + M*sigma*random.uniform(-1,1)

            self.__lPoint[i][0] = min(self.__lPoint[i][0], UBX)
            self.__lPoint[i][0] = max(self.__lPoint[i][0], self.__lPoint[i-1][0]+0.05)
            self.__lPoint[i][0] = min(self.__lPoint[i][0], UBX)


        for i in range(2,5):
            self.__uPoint[i][1] = self.__uPoint[i][1] + M*sigma*random.uniform(-1,1)
                

            self.__uPoint[i][1] = min(self.__uPoint[i][1], UBY2)
            self.__uPoint[i][1] = max(self.__uPoint[i][1], LBY2)

            

        for i in range(2, 5):
            self.__lPoint[i][1] = self.__lPoint[i][1] + M*sigma*random.uniform(-1,1)

            self.__lPoint[i][1] = min(self.__lPoint[i][1], UBY)
            self.__lPoint[i][1] = max(self.__lPoint[i][1], self.__uPoint[i][1]+0.05)
            self.__lPoint[i][1] = max(self.__lPoint[i][1], self.__uPoint[i-1][1]+0.05)

    def camber(self, g, s):
        M = np.zeros(100)
        M = (self.c_Upper+self.c_Lower)/2

        t = np.linspace(0,1,100)

        #for i in range(69):
        max_C = max(M)*100.00
        self.max_Camber = max_C

        plt.plot(self.plotX, self.plotY,'b',linewidth=2.0,label='B-spline curve')
        plt.plot(t, M,'b',linewidth=1.0,color='red',label='Camber curve %.2f---%.2f' %(self.cost,self.max_Camber))
        plt.legend(loc='best')
        plt.axis([0, 1, -0.25, 0.5])
        plt.axis('equal')
        plt.savefig(camberDirectory%(g,s))
        plt.close()
    
    def random(self):
        self.max_Camber = random.uniform(0,20)
        self.cost = random.uniform(0,200)

    def mutate(self, sigma):
        self.max_Camber = self.max_Camber +  1*sigma*random.uniform(-1,1)
        self.cost = self.cost +  10*sigma*random.uniform(-1,1)

    def mean_camber(self, g, s):
        M = np.zeros(100)
        M = (self.c_Upper+self.c_Lower)/2
        #Xi = np.linspace(0, 1, 68) 

        C = 0
        for i in range(100):
            C += (M[i]*100)
        self.max_Camber = C/100

        plt.plot(self.plotX, self.plotY,'b',linewidth=2.0,label='B-spline curve')
        plt.plot(self.c_X, M,'b',linewidth=1.0,color='red',label='Camber curve %.2f---%.2f' %(self.cost,self.max_Camber))
        plt.legend(loc='best')
        plt.axis([0, 1, -0.25, 0.5])
        plt.axis('equal')
        plt.savefig(camberDirectory%(g,s))
        plt.close()

    def error(self, og_airfoil):

        #read the og_airfoil plot
        loc = '../../optimisation_code/coord/' + og_airfoil + '.dat'
        og = np.loadtxt(loc,skiprows = 2)
        #print(og)
        x = np.array(self.plotX)
        y = np.array(self.plotY)

        print(len(og))
        #print(og[:,1])

        s = 0

        for i in range(len(og)):
                       
            if x[i] <= og[i if (i<len(og)) else (len(og)-1)][0]:
                j = i
                while x[j] < og[i if i<len(og) else (len(og)-1)][0]:
                    if(i < (len(og)/2)):
                        j-=1 #if (i<len(x)/2) else j+=1
                    else:
                        j+=1
                
                diff = y[j] - og[i if (i<len(og)) else (len(og)-1)][1]
                #print(diff)

            elif x[i] > og[i if (i<len(og)) else (len(og)-1)][0]:
                j = i
                while x[j] > og[i if (i<len(og)) else (len(og)-1)][0]:
                    if(i < (len(og)/2)):
                        j+=1 #if i<(len(x)/2) else j-=1
                    else:
                        j-=1
                
                diff = y[j] - og[i if (i<len(og)) else (len(og)-1)][1]
                #print(diff)

            s += diff**2
        #print(s)
        self.cost = 1.000/s

        plt.plot(x, y,'b',linewidth=1.0,label='Estimating A/F')
        plt.plot(self.__uPoint[:,0], self.__uPoint[:,1],'k--',label='Control polygon',marker='o',markerfacecolor='green')
       
        plt.plot(self.__lPoint[:,0],self.__lPoint[:,1],'k--',label='Control polygon',marker='o',markerfacecolor='green')
        plt.plot(og[:,0], og[:,1],'b',linewidth=1.0,color='red',label='Original A/F')
        plt.legend(loc='best')
        plt.axis([0, 1, -0.25, 0.5])
        plt.axis('equal')
        #plt.show()
        plt.savefig('error/%i--%i.svg'%(self.__generation, self.__specie))
        plt.close()