import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = ["wafer_G_B1_trans_100_3_2.csv"]
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(1, 3)
ax1t = ax[1].twinx()
legend = []
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        parsing_data = False
        Vg = []
        Id = []
        Ig = []
        for n, row in enumerate(reader):
            if row[0] == "IS":
                continue
            # Vds = 5
            # Vg.append(float(row[6]))
            # Id.append(float(row[5]))
            # Ig.append(float(row[8]))
            # Vds = 0.5
            Vg.append(float(row[6]))
            Id.append(float(row[4]))
            Ig.append(float(row[7]))
        ax[0].semilogy(Vg, np.array(Id) * 1e6 / 100)
        ax[1].plot(Vg, np.array(Id) * 1e6 / 100, color=colors[0])
        ax1t.plot(Vg[1:], np.diff(Id) / np.diff(Vg) * 1e6 / 100, color=colors[1])
        ax[2].semilogy(Vg, np.array(Ig) * 1e6 / 100)
# ax[0].legend(legend)
# ax[1].legend(legend)
ax[0].set_xlabel("Vgs [V]")
ax[1].set_xlabel("Vgs [V]")
ax[2].set_xlabel("Vgs [V]")
ax[0].set_ylabel("Id [uA/um]")
ax[1].set_ylabel("Id [uA/um]")
ax1t.set_ylabel("gm [uA/um/V]")
ax[2].set_ylabel("Ig [uA/um]")
# ax[0].set_ylim([1e-9, 1e-2])
# ax[1].set_ylim([1e-9, 1e-2])
# fig.tight_layout()
plt.show()
