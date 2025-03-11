import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

fig, ax = plt.subplots(1, 1)
legend = []
rows = {chr(i + 65): i for i in range(8)}
cols = {str(i + 1): i for i in range(8)}

resistivity = np.empty((8, 8))
resistivity[:] = np.nan

resistivity[0, 3] = 400e3
resistivity[0, 0] = 700e3
resistivity[0, 7] = 1.01e6
resistivity[7, 7] = 1.20e6
resistivity[7, 0] = 1.10e6
resistivity[3, 3] = 1.20e6
resistivity[3, 4] = 1.20e6
resistivity[1, 4] = 1.20e6
resistivity[1, 4] = 1.20e6
resistivity[1, 1] = 1.34e6

m = ax.imshow(resistivity, norm=colors.LogNorm())
ax.set_xticks(range(8), list(range(1, 9)))
ax.set_yticks(range(8), list(chr(i + 65) for i in range(8)))
cbar = plt.colorbar(m, ax=ax)
cbar.set_label("Sheet resistance (Ohm/sq)")
plt.show()
