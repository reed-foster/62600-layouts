import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

fnames = [
    # "wafer_V/wafer_V_G8_transistor_100_1_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_2_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_3_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_5_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_10_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_20_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_50_10.dat",
    # "wafer_W/wafer_W_G8_transistor_100_10_10.dat",
    # "wafer_W/wafer_W_G8_transistor_100_20_10.dat",
    # "wafer_W/wafer_W_G8_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_A1_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_A4_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_A5_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_A7_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_A8_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_C1_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_C4_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_C5_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_C7_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_C8_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_E1_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_E4_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_E5_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_E6_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_E7_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_E8_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_G1_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_G4_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_G5_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_G6_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_G7_transistor_100_50_10.dat",
    # "wafer_V/wafer_V_G8_transistor_100_50_10.dat",
    "wafer_W/wafer_W_A1_transistor_100_50_10.dat",
    "wafer_W/wafer_W_A4_transistor_100_50_10.dat",
    "wafer_W/wafer_W_A5_transistor_100_50_10.dat",
    "wafer_W/wafer_W_A8_transistor_100_50_10.dat",
    "wafer_W/wafer_W_C1_transistor_100_50_10.dat",
    "wafer_W/wafer_W_C4_transistor_100_50_10.dat",
    "wafer_W/wafer_W_C5_transistor_100_50_10.dat",
    "wafer_W/wafer_W_C8_transistor_100_50_10.dat",
    "wafer_W/wafer_W_E1_transistor_100_50_10.dat",
    "wafer_W/wafer_W_E4_transistor_100_50_10.dat",
    "wafer_W/wafer_W_E5_transistor_100_50_10.dat",
    "wafer_W/wafer_W_E8_transistor_100_50_10.dat",
    "wafer_W/wafer_W_G1_transistor_100_50_10.dat",
    # "wafer_W/wafer_W_G4_transistor_100_50_10.dat",
    "wafer_W/wafer_W_G5_transistor_100_50_10.dat",
    "wafer_W/wafer_W_G8_transistor_100_50_10.dat",
]
color_seq = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(2, 3)
legend = []


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


def alloc_data(reader):
    parsing = None
    start = 0
    stop = 0
    pts = 0
    setups = {}
    for row in reader:
        if len(row) > 0 and row[0] == "DATA:":
            break
        if len(row) > 0 and row[0] == "ID:":
            parsing = row[1]
        if parsing is not None:
            if len(row) > 0 and row[0] == "START:":
                start = float(row[1])
            if len(row) > 0 and row[0] == "STOP:":
                stop = float(row[1])
            if len(row) > 0 and row[0] == "PNTS:":
                pts = int(row[1])
            if len(row) == 0:
                setups[parsing] = np.linspace(start, stop, pts)
    return setups


SS_mVdec = np.empty((8, 8))
SS_mVdec[:] = np.nan
Vt_V = np.empty((8, 8))
Vt_V[:] = np.nan
rows = {chr(i + 65): i for i in range(8)}
cols = {str(i + 1): i for i in range(8)}

for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        chipID = fname.split("_")[3]
        W = float(fname.split("_")[-3])
        L = float(fname.split("_")[-2])
        reader = csv.reader(csvfile)
        # first get transfer curve setup
        setup = alloc_data(reader)
        Vg = setup["G"]
        Vd = setup["D"]
        Id = np.zeros((Vg.shape[0], Vd.shape[0]))
        Ig = np.zeros((Vg.shape[0], Vd.shape[0]))
        n_vg = 0
        for n, row in enumerate(reader):
            if len(row) == 0:
                continue
            if row[0] == "TEST":
                break
            if row[0] == "IS":
                continue
            Vg[n_vg] = float(row[3 * Vd.shape[0]])
            for i in range(Vd.shape[0]):
                Ig[n_vg, i] = float(row[3 * Vd.shape[0] + 1 + i])
                Id[n_vg, i] = float(row[2 * Vd.shape[0] + i])
            n_vg += 1
        if len(fnames) > 1:
            Id = Id[:, -1]
            Ig = Ig[:, -1]
            label = f"L = {L}um, Vds = {Vd[-1]}V"
            colorId = color_seq[f % len(color_seq)]
            colorIg = "k"
        else:
            label = None
            colorId = color_seq[0]
            colorIg = color_seq[1]
        ax[0, 0].semilogy(Vg, Id * 1e6 / W, ".", color=colorId, label=label)
        ax[0, 0].semilogy(Vg, Ig * 1e6 / W, ".", color=colorIg, label=None)
        ax[0, 1].plot(Vg, Id * 1e6 / W, ".", color=colorId, label=label)
        gm = (np.diff(Id, axis=0).T / np.diff(Vg)).T
        ax[1, 1].plot(
            Vg[1:],
            gm * 1e6 / W,
            ".",
            color=colorId,
            label=label,
        )
        if len(fnames) > 1:
            # get subthreshold slope
            min_I_fit = 10 * np.max(np.abs(Ig))
            max_I_fit = 50 * min_I_fit
            idx_I_min = np.argmin(np.abs(Id - min_I_fit))
            idx_I_max = np.argmin(np.abs(Id - max_I_fit))
            b, r2 = fit_xy(Vg[idx_I_min:idx_I_max], np.log(Id[idx_I_min:idx_I_max]))
            Id_est = np.exp(b[0] + b[1] * Vg)
            Id_est[Id_est > max_I_fit * 10] = np.nan
            Id_est[Id_est < min_I_fit / 10] = np.nan
            ax[0, 0].semilogy(Vg, Id_est * 1e6 / W, color=colorId, label=None)
            SS = np.log(10) / b[1]
            print(SS)
            SS_mVdec[rows[chipID[0]], cols[chipID[1]]] = SS * 1e3
            # get Vt
            max_gm_fit = np.max(np.abs(gm))
            min_gm_fit = max_gm_fit / 20
            idx_gm_min = np.argmin(np.abs(gm - min_gm_fit))
            idx_gm_max = np.argmin(np.abs(gm - max_gm_fit))
            b, r2 = fit_xy(Vg[idx_gm_min:idx_gm_max], gm[idx_gm_min:idx_gm_max])
            gm_est = b[0] + b[1] * Vg
            gm_est[gm_est > max_gm_fit * 1.1] = np.nan
            gm_est[gm_est < min_gm_fit * 0.9] = np.nan
            Vt = -b[1] / b[0]
            print(Vt)
            ax[1, 1].plot(Vg, gm_est * 1e6 / W, color=colorId, label=None)
            Vt_V[rows[chipID[0]], cols[chipID[1]]] = Vt

        setup = alloc_data(reader)
        Vd = setup["D"]
        Vg = setup["G"]
        Id = np.zeros((Vd.shape[0], Vg.shape[0]))
        Ig = np.zeros((Vd.shape[0], Vg.shape[0]))
        n_vd = 0
        for n, row in enumerate(reader):
            if len(row) == 0:
                continue
            if row[0] == "TEST":
                break
            if row[0] == "IS":
                continue
            Vd[n_vd] = float(row[Vg.shape[0]])
            for i in range(Vg.shape[0]):
                Ig[n_vd, i] = float(row[3 * Vg.shape[0] + 1 + i])
                Id[n_vd, i] = float(row[Vg.shape[0] + 1 + i])
            n_vd += 1
        if len(fnames) > 1:
            Id = Id[:, [0, -1]]
            Ig = Ig[:, [0, -1]]
            label = [f"L = {L}um, Vgs = {Vg[0]}V, {Vg[-1]}V", None]
            color = color_seq[f % len(color_seq)]
        else:
            color = color_seq[0]
            label = None
        ax[1, 0].plot(Vd, Id * 1e6 / W, ".", color=color, label=label)

# ax[0, 0].legend(loc="lower right")
# ax[1, 0].legend(loc="upper left")
# ax[0, 1].legend(loc="upper left")
# ax[1, 1].legend(loc="upper left")
ax[0, 0].set_xlabel("Vgs [V]")
ax[0, 1].set_xlabel("Vgs [V]")
ax[0, 0].set_ylabel("Id,Ig [uA/um]")
ax[0, 1].set_ylabel("Id [uA/um]")
ax[1, 1].set_xlabel("Vgs [V]")
ax[1, 1].set_ylabel("gm [uA/um/V]")
_, top = ax[1, 1].get_ylim()
ax[1, 1].set_ylim([-0.1 * top, top])
ax[1, 0].set_xlabel("Vds [V]")
ax[1, 0].set_ylabel("Id [uA/um]")
plt.suptitle(fnames[0])
# ax[0].set_ylim([1e-9, 1e-2])
# ax[1].set_ylim([1e-9, 1e-2])
# fig.tight_layout()
m = ax[0, 2].imshow(SS_mVdec)
ax[0, 2].set_title("subthreshold slope (mV/dec)")
ax[0, 2].set_xticks(range(8), list(range(1, 9)))
ax[0, 2].set_yticks(range(8), list(chr(i + 65) for i in range(8)))
cbar = plt.colorbar(m, ax=ax[0, 2])
m = ax[1, 2].imshow(Vt_V)
ax[1, 2].set_title("Threshold voltage (V)")
ax[1, 2].set_xticks(range(8), list(range(1, 9)))
ax[1, 2].set_yticks(range(8), list(chr(i + 65) for i in range(8)))
cbar = plt.colorbar(m, ax=ax[1, 2])
plt.show()
