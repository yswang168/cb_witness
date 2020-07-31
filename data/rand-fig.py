import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

figure = plt.figure()
ax = plt.axes(projection='3d')

X = np.arange(50,201,10)
Y = np.arange(3.0,5.1,0.1)

x,y = np.meshgrid(X,Y)
z = np.loadtxt("50-200.txt")[:,2].reshape((21,16))

#X,Y = np.meshgrid(X,Y)
#ax.plot_wireframe(X,Y,Z1D)

ax.plot_surface(x,y,z,rstride=1,cstride=1,cmap='rainbow')
# get the time 
#plt.legend()                   


ax.set_title('Time(s)')
ax.set_ylabel('ratio')
ax.set_xlabel('Number of variables')
'''
plt.zlabel('Tims(s)')
plt.ylabel('Ration')        
plt.xlabel('Number of variables (n)')
'''
plt.savefig("rand-50-200.png")

z = np.loadtxt("50-200-MUS.txt")[:,2].reshape((21,16))
ax.plot_surface(x,y,z,rstride=1,cstride=1,cmap='rainbow')
plt.savefig("rand-50-200-MUS.png")
