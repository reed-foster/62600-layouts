import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "wafer_O/wafer_O_D4_TLM_100.dat",
    "wafer_O/wafer_O_D4_TLM_10.dat",
    "wafer_O/wafer_O_D4_TLM_150.dat",
    "wafer_O/wafer_O_D4_TLM_20.dat",
    "wafer_O/wafer_O_D4_TLM_50.dat",
    "wafer_O/wafer_O_D4_TLM_80.dat",
    # "wafer_O/wafer_O_D4_itores_100_2.dat",
    # "wafer_O/wafer_O_D4_itores_100_5.dat",
    # "wafer_O/wafer_O_D4_itores_100_10.dat",
    # "wafer_O/wafer_O_D4_itores_100_20.dat",
    # "wafer_O/wafer_O_D4_itores_100_50.dat",
    # "wafer_O/wafer_O_D4_itores_100_100.dat",
    # "wafer_O/wafer_O_D4_itores_10_2.dat",
    # "wafer_O/wafer_O_D4_itores_10_5.dat",
    # "wafer_O/wafer_O_D4_itores_10_10.dat",
    # "wafer_O/wafer_O_D4_itores_10_20.dat",
    # "wafer_O/wafer_O_D4_itores_10_50.dat",
    # "wafer_O/wafer_O_D4_itores_10_100.dat",
    # "wafer_A/wafer_A_A1_itores_100_25_hr.dat",
    # "wafer_A/wafer_A_A1_itores_100_2_hr.dat",
    # "wafer_A/wafer_A_A1_itores_100_5_hr.dat",
    # "wafer_A/wafer_A_A1_itores_10_25_hr.dat",
    # "wafer_A/wafer_A_A1_itores_10_2_hr.dat",
    # "wafer_A/wafer_A_A1_itores_10_5_hr.dat",
    # "wafer_G/wafer_G_A1_itores_100_10.dat",
    # "wafer_G/wafer_G_A1_itores_100_2.dat",
    # "wafer_G/wafer_G_A1_itores_100_25.dat",
    # "wafer_G/wafer_G_C1_itores_100_2_reversed.dat",
    # "wafer_G/wafer_G_A1_itores_10_2.dat",
    # "wafer_G/wafer_G_A1_itores_10_25.dat",
    # "wafer_G/wafer_G_C1_itores_10_2.dat",
    # "wafer_G/wafer_G_C1_itores_10_25.dat",
    # "wafer_G/wafer_G_C1_itores_50_2.dat",
    # "wafer_G/wafer_G_C1_itores_50_25.dat",
    # "wafer_G/wafer_G_C1_itores_50_2_higher_V.dat",
    # "wafer_G/wafer_G_A1_itores_100_10.dat",
    # "wafer_G/wafer_G_A1_itores_100_2.dat",
    # "wafer_G/wafer_G_A1_itores_100_25.dat",
    # "wafer_G/wafer_G_A1_itores_10_2.dat",
    # "wafer_G/wafer_G_A1_itores_10_25.dat",
    # "wafer_G/wafer_G_C1_itores_100_2.dat",
    # "wafer_G/wafer_G_C1_itores_100_2_reversed.dat",
    # "wafer_G/wafer_G_C1_itores_10_2.dat",
    # "wafer_G/wafer_G_C1_itores_10_25.dat",
    # "wafer_G/wafer_G_C1_itores_50_2.dat",
    # "wafer_G/wafer_G_C1_itores_50_25.dat",
    # "wafer_G/wafer_G_C1_itores_50_2_higher_V.dat",
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


def get_scale_sw(R):
    if R > 1e9:
        return 1e9, "G"
    if R > 1e6:
        return 1e6, "M"
    if R > 1e3:
        return 1e3, "k"
    return 1, ""


color_seq = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(1, 2)
L_list = []
res_list = []
max_I = -1
min_I = 1
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        if "TLM" in fname:
            W, L = 50, float(fname.split("/")[-1].split(".")[0].split("_")[4])
        else:
            W, L = map(float, fname.split("/")[-1].split(".")[0].split("_")[4:6])
        reader = csv.reader(csvfile)
        V = []
        I = []
        data = False
        row_len = 0
        for n, row in enumerate(reader):
            if data:
                if len(row) < row_len:
                    data = False
                    continue
                V.append(float(row[1]))
                I.append(float(row[2]))
            else:
                if len(row) == 0 or row[0] != "IA":
                    continue
                row_len = len(row)
                data = True
        # fit IV to resistor
        I = np.array(I)
        V = np.array(V)
        # Ifit = I[np.abs(V) < 0.5]
        # Vfit = V[np.abs(V) < 0.5]
        Ifit = I[(V > 0)]
        Vfit = V[(V > 0)]
        b, r2 = fit_xy(Ifit, Vfit)
        L_list.append(L * 1e-6)  # m
        res_list.append(b[1] * W * 1e-6)  # ohm*m

        print(fname)
        print(f"L = {L}, R = {b[1]} (r^2 = {r2})")

        scale, sw = get_scale_sw(b[1])
        name = f"W/L = {W}/{L}, R = {round(b[1]/scale)}{sw}Ohm"
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
res_list = np.array(res_list)  # ohm*m
L_list = np.array(L_list)  # m
b, r2 = fit_xy(L_list, res_list)
print(b)
Rc = b[0] / 2  # ohm*m
Lt = b[0] / b[1] / 2  # m
Rsheet = b[1]  # ohm
rho_c = Rsheet * Lt**2  # ohm*m^2
scale, sw = get_scale_sw(Rsheet)
print(Rc)
print(Lt)
L_smooth = np.linspace(-2 * Lt, 1.1 * np.max(L_list), 10)
ax[1].plot(L_list * 1e6, res_list / scale * 1e6, ".", color="k")
label = f"Rc = {round(Rc/scale*1e6)}{sw}Ohm*um"
label += f"\nRsq = {round(Rsheet/scale)}{sw}Ohm"
label += f"\nLt = {round(Lt*1e6,2)}um"
label += f"\nrho_c = {round(rho_c*1e12/scale)}{sw}Ohm*um^2"
ax[1].plot(
    L_smooth * 1e6, (b[0] + b[1] * L_smooth) / scale * 1e6, "--", color="k", label=label
)
ax[1].legend()
ax[1].set_xlabel("length [um]")
ax[1].set_ylabel(f"R [{sw}Ohm*um]")
# ax[1].set_ylim([0,100])
# ax[1].set_xlim([-1,1])
plt.show()
