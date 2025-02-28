import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "wafer_J_A1_itores_100_2.dat",
    "wafer_J_A1_itores_10_2.dat",
    "wafer_J_A1_itores_20_2.dat",
    "wafer_J_A1_itores_50_2.dat",
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
res = {}
sq = {}
max_I = -1
min_I = 1
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        W, L = map(float, fname.split(".")[0].split("_")[4:6])
        reader = csv.reader(csvfile)
        V = []
        I = []
        data = False
        for n, row in enumerate(reader):
            if data:
                if len(row) < 3:
                    data = False
                    break
                    # continue
                V.append(float(row[1]))
                I.append(float(row[2]))
            else:
                if len(row) < 3 or row[0] != "IA":
                    continue
                data = True
        # fit IV to resistor
        middle = len(I) // 2
        size = 2 * (len(I) // 2)
        b, r2 = fit_xy(
            I[middle - size // 2 : middle + size // 2],
            V[middle - size // 2 : middle + size // 2],
        )
        if W not in sq:
            sq[W] = []
            res[W] = []
        sq[W].append(L / W)
        res[W].append(b[1])
        print(fname)
        print(f"W/L = {W}/{L}, R = {b[1]} (r^2 = {r2})")

        name = f"{W}/{L} - R = {round(b[1]/1e9)}G"
        max_I = max(max_I, np.max(I))
        min_I = min(min_I, np.min(I))
        ax[0].plot(
            V, np.array(I) * 1e9, ".", color=color_seq[f % len(color_seq)], label=name
        )
        ax[0].set_xlim([np.min(V), np.max(V)])
        ax[0].set_ylim([min_I * 1e9, max_I * 1e9])
        ilist = np.linspace(np.min(I), np.max(I), 100)
        ax[0].plot(
            ilist * b[1] + b[0], ilist * 1e9, "-", color=color_seq[f % len(color_seq)]
        )
ax[0].set_xlabel("V [V]")
ax[0].set_ylabel("I [nA]")
# ax[0].set_xlim([-2,2])
ax[0].legend()
legend = []
sq_flat = []
res_flat = []
for n, W in enumerate(sq.keys()):
    ax[1].plot(sq[W], np.array(res[W]) / 1e9, ".", color=color_seq[n])
    legend.append(f"W = {W}")
    b, r2 = fit_xy(sq[W], res[W])
    sqlist = np.linspace(np.min(sq[W]), np.max(sq[W]), 100)
    ax[1].plot(sqlist, (b[0] + b[1] * sqlist) / 1e9, "--", color=color_seq[n])
    Rc = b[0] / 2 * W
    legend.append(f"(W = {W}) Rc = {round(Rc/1e9)}GOhm*um, Rsq = {round(b[1]/1e9)}G")
    sq_flat += sq[W]
    res_flat += res[W]
b, r2 = fit_xy(sq_flat, res_flat)
sqlist = np.linspace(np.min(sq_flat), np.max(sq_flat), 100)
ax[1].plot(sqlist, (b[0] + b[1] * sqlist) / 1e9, "--", color="k")
Rc = b[0] / 2 * W
legend.append(f"(overall) Rc = {round(Rc/1e9)}GOhm*um, Rsq = {round(b[1]/1e9)}G")
# ax[1].legend(legend)
ax[1].set_xlabel("squares (L/W)")
ax[1].set_ylabel("R [GOhm]")
plt.show()
