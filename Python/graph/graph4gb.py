from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

x = []
y = []
z = []

# 0
# x = [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300]
# y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# z = [100, 100, 100, 100, 100, 100, 100, 100, 97, 100, 98, 89]
#1
x = x + [1750, 1800, 1850]
y = y + [1, 1, 1]
z = z + [100, 99, 72]
#2
x = x + [1750, 1800, 1850, 1900]
y = y + [2, 2, 2, 2]
z = z + [100, 100, 100, 90]
#3
x = x + [1750, 1800, 1850, 1900, 1950, 2000]
y = y + [3, 3, 3, 3, 3, 3]
z = z + [100, 100, 100, 100, 99, 98]
#4
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050]
y = y + [4, 4, 4, 4, 4, 4, 4]
z = z + [100, 100, 100, 100, 100, 100, 97]
#5
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150]
y = y + [5, 5, 5, 5, 5, 5, 5, 5, 5]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 93]
#6
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250]
y = y + [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
#7
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300]
y = y + [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 100, 99, 95, 60]
#8
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250]
y = y + [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 100, 99, 98]

top = z
bottom = np.zeros_like(top)
width = 50
depth = 1

colourMap = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu)
colourMap.set_array(top)
norm = plt.Normalize((top/np.log10(max(top))).min(), (top/np.log10(max(top))).max())
colours = plt.cm.RdYlBu(norm(top/np.log10(max(top))))
colBar = plt.colorbar(colourMap).set_label('Execuções completadas')
ax.bar3d(x, y, bottom, width, depth, top, shade=True, color=colours)
font1 = {'family':'serif','color':'black','size':13}

plt.xlabel('Frequência (Hz)', fontdict=font1)
plt.ylabel('Overvoltage', fontdict=font1)
ax.set_title('Raspberry 4GB')
plt.show()