import numpy as np
import matplotlib.pyplot as plt

def camber(self, g, s):
    M = np.zeros(68)
    M = self.c_Upper+self.c_Lower
    plt.plot(self.plotX, self.plotY,'b',linewidth=2.0,label='B-spline curve')
    plt.plot(self.plotX, M,'b',linewidth=2.0,label='Camber curve')
    plt.legend(loc='best')
    plt.axis([0, 1, -0.25, 0.5])
    plt.axis('equal')
    plt.savefig('Camber/airfoil_%i-%i.png'%(g,s))