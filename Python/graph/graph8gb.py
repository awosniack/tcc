from turtle import color
import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
x = []
y = []
z = []
# 0
# x = [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250]
# y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# z = [100, 99, 100, 100, 100, 100, 100, 100, 90, 83, 26]
#1
x = x + [1750, 1800, 1850]
y = y + [1, 1, 1]
z = z + [100, 94, 28]
#2
x = x + [1750, 1800, 1850, 1900]
y = y + [2, 2, 2, 2]
z = z + [100, 100, 100, 87]
#3
x = x + [1750, 1800, 1850, 1900, 1950, 2000]
y = y + [3, 3, 3, 3, 3, 3]
z = z + [100, 100, 100, 100, 99, 96]
#4
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050]
y = y + [4, 4, 4, 4, 4, 4, 4]
z = z + [100, 100, 100, 100, 100, 100, 96]
#5
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150]
y = y + [5, 5, 5, 5, 5, 5, 5, 5, 5]
z = z + [100, 100, 100, 100, 100, 100, 100, 96, 95]
#6
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200]
y = y + [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 91, 33]
#7
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250]
y = y + [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 100, 95, 33]
#8
x = x + [1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300]
y = y + [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
z = z + [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 27]

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
ax.set_title('Raspberry 8GB')
plt.show()