import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "wafer_M_A1_TLM_10_fine.dat",
    "wafer_M_A1_TLM_20_fine.dat",
    "wafer_M_A1_TLM_50_fine.dat",
    "wafer_M_A1_TLM_80_fine.dat",
    "wafer_M_A1_TLM_100_fine.dat",
    "wafer_M_A1_TLM_150_fine.dat",
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
L_list = []
res_list = []
max_I = -1
min_I = 1
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        L = float(fname.split(".")[0].split("_")[4])
        reader = csv.reader(csvfile)
        V = []
        I = []
        data = False
        for n, row in enumerate(reader):
            if data:
                if len(row) < 8:
                    data = False
                    continue
                V.append(float(row[3]))
                I.append(float(row[6]))
            else:
                if len(row) < 8 or row[0] != "IS":
                    continue
                data = True
        # fit IV to resistor
        Ifit = []
        Vfit = []
        middle = len(I) // 2
        size = len(I) // 32
        for i in range(len(I)):
            if i < middle:
                continue
            # if i > middle + 8 * size:
            # continue
            Ifit.append(I[i])
            Vfit.append(V[i])
        b, r2 = fit_xy(Ifit, Vfit)
        L_list.append(L)
        res_list.append(b[1])

        print(fname)
        print(f"L = {L}, R = {b[1]} (r^2 = {r2})")

        name = f"{L} - R = {round(b[1]/1e6)}M"
        max_I = max(max_I, np.max(I))
        min_I = min(min_I, np.min(I))
        ax[0].plot(
            V, np.array(I) * 1e6, ".", color=color_seq[f % len(color_seq)], label=name
        )
        ax[0].set_xlim([np.min(V), np.max(V)])
        # ax[0].set_ylim([min_I * 1e6, max_I * 1e9])
        ilist = np.linspace(np.min(I), np.max(I), 1000)
        ax[0].plot(
            ilist * b[1] + b[0], ilist * 1e6, "-", color=color_seq[f % len(color_seq)]
        )
ax[0].set_xlabel("V [V]")
ax[0].set_ylabel("I [uA]")
# ax[0].set_xlim([-2,2])
ax[0].legend()
b, r2 = fit_xy(L_list, res_list)
L_smooth = np.linspace(np.min(L_list), np.max(L_list), 100)
Rc = b[0] / 2
ax[1].plot(L_list, np.array(res_list) / 1e9, ".", color="k")
ax[1].plot(
    L_smooth,
    (b[0] + b[1] * L_smooth) / 1e9,
    "--",
    color="k",
    label=f"(overall) Rc = {round(Rc*50/1e9)}GOhm*um, Rsq = {round(b[1]*50/1e9)}G",
)
ax[1].legend()
ax[1].set_xlabel("length (L)")
ax[1].set_ylabel("R [GOhm]")
plt.show()
