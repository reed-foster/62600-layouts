import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    # "wafer_A_A1_itores_10_2_hr.dat",
    # "wafer_A_A1_itores_10_5_hr.dat",
    # "wafer_A_A1_itores_10_25_hr.dat",
    # "wafer_A_A1_itores_100_2_hr.dat",
    # "wafer_A_A1_itores_100_5_hr.dat",
    # "wafer_A_A1_itores_100_25_hr.dat",
    "wafer_B_A1_itores_10_2.dat",
    "wafer_B_A1_itores_10_5.dat",
    "wafer_B_A1_itores_10_25.dat",
    "wafer_B_A1_itores_100_2.dat",
    "wafer_B_A1_itores_100_5.dat",
    "wafer_B_A1_itores_100_25.dat",
    # "wafer_B_E10_itores_10_2.dat",
    # "wafer_B_E10_itores_10_5.dat",
    ##"wafer_B_E10_itores_10_25.dat",
    # "wafer_B_E10_itores_10_25_hr.dat",
    # "wafer_B_E10_itores_100_2_hr.dat",
    # "wafer_B_E10_itores_100_5_hr.dat",
    # "wafer_B_E10_itores_100_25_hr.dat",
    # "wafer_G_C1_itores_10_2.dat",
    # "wafer_G_C1_itores_10_25.dat",
    # "wafer_G_C1_itores_50_2.dat",
    # "wafer_G_C1_itores_50_25.dat",
    # "wafer_G_C1_itores_100_2.dat",
    # "wafer_G_C1_itores_100_25.dat",
    # "wafer_G_A1_itores_10_2.dat",
    # "wafer_G_A1_itores_100_2.dat",
    # "wafer_G_A1_itores_10_25.dat",
    # "wafer_G_A1_itores_100_25.dat",
    # "wafer_G_A1_itores_100_10.dat",
    # "wafer_G_C1_itores_50_2_higher_V.dat",
    # "wafer_G_C1_itores_100_2_reversed.dat",
]


def fit_xy(xdata, ydata):
    X = np.ones((len(xdata), 2))
    X[:, 1] = np.array(xdata)
    y = np.array(ydata)
    b, residuals, _, _ = np.linalg.lstsq(X, y)
    r2 = 1 - sum((b[0] + b[1] * xi - yi) ** 2 for xi, yi in zip(xdata, ydata)) / sum(
        (yi - np.mean(y)) ** 2 for yi in ydata
    )
    return b, r2


colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(1, 2)
legend = []
res = {}
sq = {}
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
                    break
                V.append(float(row[1]))
                I.append(float(row[2]))
            else:
                if len(row) < 3 or row[0] != "IA":
                    continue
                data = True
        # fit IV to resistor
        middle = len(I) // 2
        size = 2 * (len(I) // 16)
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

        legend.append(f"{W}/{L} - R = {round(b[1]/1e3)}k")
        ax[0].plot(V, np.array(I) * 1e6)
ax[0].set_xlabel("V [V]")
ax[0].set_ylabel("I [uA]")
ax[0].set_xlim([-2, 2])
ax[0].legend(legend)
legend = []
for n, W in enumerate(sq.keys()):
    ax[1].plot(sq[W], np.array(res[W]) / 1e3, ".", color=colors[n])
    b, r2 = fit_xy(sq[W], res[W])
    sqlist = np.linspace(np.min(sq[W]), np.max(sq[W]), 100)
    ax[1].plot(sqlist, (b[0] + b[1] * sqlist) / 1e3, "--", color=colors[n])
    Rc = b[0] / 2 * W
    legend.append(f"W = {W}")
    legend.append(f"Rc = {round(Rc/1e3)}kOhm*um, Rsq = {round(b[1]/1e6)}k")
ax[1].legend(legend)
ax[1].set_xlabel("squares (L/W)")
ax[1].set_ylabel("R [kOhm]")
plt.show()
