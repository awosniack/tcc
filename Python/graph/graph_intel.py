import matplotlib.pyplot as plt
import numpy as np
import os

def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
plt.style.use('_mpl-gallery')

# make data
np.random.seed(1)
y = np.arange(1375, 1560, 25)
x1 = [
    # 2200,
    1750, 1850, 1900, 2000, 2100, 2250, 2150, 2150]
x2 = [
    # 2300,
    1850, 1900, 2000, 2050, 2150, 2260, 2300, 2250]

# plot
fig, ax = plt.subplots()

ax.plot(x1, y, '-o', color='blue', label='Limite tensão segura')
ax.plot(x2, y, '-s', color='red', label='Limite tensão falha')
ax.fill_betweenx(y, x2, 2400, alpha=.5, linewidth=1, facecolor='red', label='Tensão falha')
ax.fill_betweenx(y, x1, x2, facecolor='none', hatch='\\', edgecolor='red', label='Tensão perigosa')
ax.fill_betweenx(y, 1300, x1, alpha=.5, linewidth=1, label = 'Tensão segura')
ax.plot(1900, 1400, '*', color='green', label='Tensão escolhida')
ax.set_xlabel('Frequência (MHz)')
ax.set_ylabel('Tensão (mV)')
ax.set_title('Raspberry 4GB')
ax.margins(y=0, x=0)
ax.legend()

# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

plt.subplots_adjust(left=0.2,bottom=0.2, top = 0.9, right = 0.9)
fig.set_size_inches(7, 5)
createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', 'tabela'))
plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', 'tabela', '4gb'), dpi=300)


x1 = [
    # 2200,
    1750, 1850, 1900, 2000, 2050, 2100, 2150, 2250]
x2 = [
    # 2300,
    1850, 1900, 2000, 2050, 2150, 2200, 2250, 2300]

plt.figure(2)

fig, ax = plt.subplots()

ax.plot(x1, y, '-o', color='blue', label='Limite tensão segura')
ax.plot(x2, y, '-s', color='red', label='Limite tensão falha')
ax.fill_betweenx(y, x2, 2400, alpha=.5, linewidth=1, facecolor='red', label='Tensão falha')
ax.fill_betweenx(y, x1, x2, facecolor='none', hatch='\\', edgecolor='red', label='Tensão perigosa')
ax.fill_betweenx(y, 1300, x1, alpha=.5, linewidth=1, label = 'Tensão segura')
ax.plot(1900, 1400, '*', color='green', label='Tensão escolhida')
ax.set_xlabel('Frequência (MHz)')
ax.set_ylabel('Tensão (mV)')
ax.set_title('Raspberry 8GB')
ax.margins(y=0, x=0)
ax.legend()

# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

plt.subplots_adjust(left=0.2,bottom=0.2, top = 0.9, right = 0.9)
fig.set_size_inches(7, 5)
createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', 'tabela'))
plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', 'tabela', '8gb'), dpi=300)

