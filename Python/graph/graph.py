from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


fig = plt.figure()

ax1 = fig.add_subplot(111, projection='3d')
ax2 = fig.add_subplot(121, projection='3d')
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
ax1.bar3d(x, y, bottom, width, depth, top, shade=True, color=colours)
font1 = {'family':'serif','color':'black','size':13}


x2 = []
y2 = []
z2 = []
# 0
# x2 = [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250]
# y2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# z2 = [100, 99, 100, 100, 100, 100, 100, 100, 90, 83, 26]
#1
x2 = x2 + [1750, 1800, 1850]
y2 = y2 + [1, 1, 1]
z2 = z2 + [100, 94, 28]
#2
x2 = x2 + [1750, 1800, 1850, 1900]
y2 = y2 + [2, 2, 2, 2]
z2 = z2 + [100, 100, 100, 87]
#3
x2 = x2 + [1750, 1800, 1850, 1900, 1950, 2000]
y2 = y2 + [3, 3, 3, 3, 3, 3]
z2 = z2 + [100, 100, 100, 100, 99, 96]
#4
x2 = x2 + [1750, 1800, 1850, 1900, 1950, 2000, 2050]
y2 = y2 + [4, 4, 4, 4, 4, 4, 4]
z2 = z2 + [100, 100, 100, 100, 100, 100, 96]
#5
x2 = x2 + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150]
y2 = y2 + [5, 5, 5, 5, 5, 5, 5, 5, 5]
z2 = z2 + [100, 100, 100, 100, 100, 100, 100, 96, 95]
#6
x2 = x2 + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200]
y2 = y2 + [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
z2 = z2 + [100, 100, 100, 100, 100, 100, 100, 100, 91, 33]
#7
x2 = x2 + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250]
y2 = y2 + [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
z2 = z2 + [100, 100, 100, 100, 100, 100, 100, 100, 100, 95, 33]
#8
x2 = x2 + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300]
y2 = y2 + [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
z2 = z2 + [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 27]

top2 = z2
bottom2 = np.zeros_like(top2)
width2 = 50
depth2 = 1

colourMap2 = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu)
colourMap2.set_array(top2)
norm2 = plt.Normalize((top2/np.log10(max(top2))).min(), (top2/np.log10(max(top2))).max())
colours2 = plt.cm.RdYlBu(norm(top2/np.log10(max(top2))))
colBar2 = plt.colorbar(colourMap2).set_label('Execuções completadas')
ax2.bar3d(x2, y2, bottom2, width2, depth2, top2, shade=True, color=colours2)


plt.xlabel('Frequência (Hz)', fontdict=font1)
plt.ylabel('Overvoltage', fontdict=font1)
ax1.set_title('Raspberry 4GB')
ax2.set_title('Raspberry 8GB')
plt.show()