import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "20250206/2_6_2025 10_03_32 AM;waferB_transistor_100_25_10_A1;62600 IdVg(1);.csv",
]
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

fig, ax = plt.subplots(1, 2)
ax1t = ax[1].twinx()
legend = []
for f, fname in enumerate(fnames):
    n_max = 0
    with open(fname) as csvfile:
        n_max = sum(1 for row in csv.reader(csvfile))
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        parsing_data = False
        Vg = []
        Id = []
        Ig = []
        num_rows = 0
        for n, row in enumerate(reader):
            if n < 460:
                continue
            if row[0] != "DataValue" or (n == n_max - 1) or (num_rows == 101):
                parsing_data = False
                devname = fname.split(";")[1]
                W = float(devname.split("_")[2])
                ax[0].semilogy(Vg, np.array(Id) / W * 1e6)
                ax[1].plot(Vg, np.array(Id) / W * 1e6)
                ax1t.plot(
                    Vg[1:],
                    np.array(np.diff(Id) / np.diff(Vg)) / W * 1e6,
                    color=colors[1],
                )
                # ax[0].plot(Vg, np.array(Id)/W*1e6)
                # ax[1].semilogy(Vg, np.array(Ig)/W*1e6)
                legend.append("_".join(devname.split("_")[2:]))
                # print(f'{devname}: Ig,max = %s' % float('%.2g' % np.max(np.abs(Ig))))
                Vg = []
                Id = []
                Ig = []
            else:
                num_rows += 1
                Vg.append(float(row[1]))
                Id.append(float(row[3]))
                Ig.append(float(row[5]))

# ax[0].legend(legend)
# ax[1].legend(legend)
ax[0].set_xlabel("Vgs [V]")
ax[1].set_xlabel("Vgs [V]")
ax[0].set_ylabel("Id [uA/um]")
ax[1].set_ylabel("Id [uA/um]", color=colors[0])
ax1t.set_ylabel("gm [uA/um/V]", color=colors[1])
ax[0].set_ylim([1e-8, 1e-2])
ax1t.tick_params(axis="y", labelcolor=colors[1])
ax[1].tick_params(axis="y", labelcolor=colors[0])
plt.show()
