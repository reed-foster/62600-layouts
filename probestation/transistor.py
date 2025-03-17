import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "wafer_V/wafer_V_G8_transistor_100_1_10.dat",
    "wafer_V/wafer_V_G8_transistor_100_2_10.dat",
    "wafer_V/wafer_V_G8_transistor_100_3_10.dat",
    "wafer_V/wafer_V_G8_transistor_100_5_10.dat",
    "wafer_V/wafer_V_G8_transistor_100_10_10.dat",
    "wafer_V/wafer_V_G8_transistor_100_20_10.dat",
    "wafer_V/wafer_V_G8_transistor_100_50_10.dat",
    # "wafer_W/wafer_W_G8_transistor_100_10_10.dat",
    # "wafer_W/wafer_W_G8_transistor_100_20_10.dat",
    # "wafer_W/wafer_W_G8_transistor_100_50_10.dat",
]
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(2, 2)
legend = []


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


for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
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
            colorId = colors[f]
            colorIg = "k"
        else:
            label = None
            colorId = colors[0]
            colorIg = colors[1]
        ax[0, 0].semilogy(Vg, Id * 1e6 / W, ".", color=colorId, label=label)
        ax[0, 0].semilogy(Vg, Ig * 1e6 / W, ".", color=colorIg, label=None)
        ax[0, 1].plot(Vg, Id * 1e6 / W, ".", color=colorId, label=label)
        ax[1, 1].plot(
            Vg[1:],
            (np.diff(Id, axis=0).T / np.diff(Vg)).T * 1e6 / W,
            ".",
            color=colorId,
            label=label,
        )
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
            color = colors[f]
        else:
            color = colors[0]
            label = None
        ax[1, 0].plot(Vd, Id * 1e6 / W, ".", color=color, label=label)

ax[0, 0].legend(loc="lower right")
ax[1, 0].legend(loc="upper left")
ax[0, 1].legend(loc="upper left")
ax[1, 1].legend(loc="upper left")
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
plt.show()
