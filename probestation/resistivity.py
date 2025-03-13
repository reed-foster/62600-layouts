import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

fnames = [
    "wafer_Q/resistivity.dat",
    "wafer_O/resistivity.dat",
    "wafer_S/resistivity.dat",
    "wafer_R/resistivity.dat",
]


def get_scale_sw(R):
    if R > 1e9:
        return 1e9, "G"
    if R > 1e6:
        return 1e6, "M"
    if R > 1e3:
        return 1e3, "k"
    return 1, ""


rows = {chr(i + 65): i for i in range(8)}
cols = {str(i + 1): i for i in range(8)}

n_rows = int(round(len(fnames) ** 0.5))
n_cols = (len(fnames) + n_rows - 1) // n_rows

fig, ax = plt.subplots(n_rows, n_cols)

row_i = 0
col_i = 0
for f, fname in enumerate(fnames):
    resistivity = np.empty((8, 8))
    resistivity[:] = np.nan
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        for n, row in enumerate(reader):
            resistivity[rows[row[0][0]], cols[row[0][1]]] = float(row[1])

    m = ax[row_i, col_i].imshow(resistivity)
    # m = ax[row_i,col_i].imshow(resistivity), norm=colors.LogNorm())
    ax[row_i, col_i].set_xticks(range(8), list(range(1, 9)))
    ax[row_i, col_i].set_yticks(range(8), list(chr(i + 65) for i in range(8)))
    cbar = plt.colorbar(m, ax=ax[row_i, col_i])
    mean_R = np.nanmean(resistivity)
    std_R = np.nanstd(resistivity)
    scale, sw = get_scale_sw(mean_R)
    ax[row_i, col_i].set_title(
        f"{fname.split('/')[0]}: {round(mean_R/scale,1)}{sw}Ohm ± {round(std_R/scale,2)}{sw}Ohm"
    )

    col_i += 1
    if col_i == n_cols:
        col_i = 0
        row_i += 1

plt.show()
