import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

fnames = [
    "wafer_B_A1_4probe.dat",
    "wafer_B_B1_4probe.dat",
    "wafer_B_C1_4probe.dat",
    "wafer_B_C5_4probe.dat",
    "wafer_B_C6_4probe.dat",
    "wafer_B_D5_4probe.dat",
    "wafer_B_D6_4probe.dat",
    "wafer_B_E10_4probe.dat",
]


def fit_xy(xdata, ydata):
    X = np.ones((len(xdata), 2))
    X[:, 1] = np.array(xdata)
    y = np.array(ydata)
    b, residuals, _, _ = np.linalg.lstsq(X, y)
    if sum((yi - np.mean(y)) ** 2 for yi in ydata) == 0:
        r2 = 0
    else:
        r2 = 1 - sum(
            (b[0] + b[1] * xi - yi) ** 2 for xi, yi in zip(xdata, ydata)
        ) / sum((yi - np.mean(y)) ** 2 for yi in ydata)
    return b, r2


color_seq = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(1, 2)
legend = []
rows = {chr(i + 65): i for i in range(5)}
cols = {str(i + 1): i for i in range(10)}

resistivity = np.empty((5, 10))
resistivity[:] = np.nan

for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        V = []
        I = []
        data = False
        for n, row in enumerate(reader):
            if data:
                if len(row) < 4:
                    data = False
                    continue
                V.append(float(row[2]) - float(row[3]))
                I.append(float(row[0]))
            else:
                if len(row) < 4 or row[0] != "IF2P":
                    continue
                data = True
        # fit IV to resistor
        middle = len(I) // 2
        size = 2 * (len(I) // 16)
        b, r2 = fit_xy(
            I[middle - size // 2 : middle + size // 2],
            V[middle - size // 2 : middle + size // 2],
        )
        cellname = fname.split("_")[2]
        resistivity[rows[cellname[0]], cols[cellname[1]]] = b[1]
        print(fname)
        print(f"Rsheet = {b[1]}, r^2={r2}")

        ax[0].plot(
            V,
            np.array(I) * 1e9,
            ".",
            color=color_seq[f % len(color_seq)],
            label=cellname,
        )
        ilist = np.linspace(np.min(I), np.max(I), 100)
        ax[0].plot(
            ilist * b[1] + b[0], ilist * 1e9, "-", color=color_seq[f % len(color_seq)]
        )
ax[0].set_xlabel("V [V]")
ax[0].set_ylabel("I [nA]")
ax[0].legend(ncol=2)
m = ax[1].imshow(resistivity, norm=colors.LogNorm())
ax[1].set_xticks(range(10), list(range(1, 11)))
ax[1].set_yticks(range(5), list(chr(i + 65) for i in range(5)))
ax[1].set_aspect("equal")
cbar = plt.colorbar(m, ax=ax[1])
cbar.set_label("Sheet resistance (Ohm/sq)")
plt.show()
