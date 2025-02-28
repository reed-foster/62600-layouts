import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "wafer_G_A1_transistor_100_2_2.dat",
    # "wafer_G_A1_transistor_100_25_2.dat",
    # "wafer_G_A1_transistor_100_2_5_damaged.dat",
    # "wafer_G_A1_transistor_100_3_2.dat",
    # "wafer_G_A1_transistor_100_5_2.dat",
    # "wafer_G_A8_transistor_100_10_2.dat",
    # "wafer_G_A8_transistor_100_2_2.dat",
    # "wafer_G_A8_transistor_100_25_2_again.dat",
    # "wafer_G_A8_transistor_100_25_2.dat",
    # "wafer_G_A8_transistor_100_5_2.dat",
    # "wafer_G_E4_transistor_100_10_2.dat",
    # "wafer_G_E4_transistor_100_2_2.dat",
    # "wafer_G_E4_transistor_100_25_2.dat",
    # "wafer_G_E4_transistor_100_3_2.dat",
    # "wafer_G_E4_transistor_100_5_2_broken.dat",
    # "wafer_G_H8_transistor_100_10_2.dat",
    # "wafer_G_H8_transistor_100_2_2.dat",
    # "wafer_G_H8_transistor_100_25_2_again.dat",
    # "wafer_G_H8_transistor_100_25_2.dat",
    # "wafer_G_H8_transistor_100_2_5.dat",
    # "wafer_G_H8_transistor_100_5_2.dat",
]
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fig, ax = plt.subplots(2, 2)
# ax01t = ax[0,1].twinx()
legend = []
for f, fname in enumerate(fnames):
    num_Vg = 0
    data = False
    row_len = -1
    num_Vd = 1
    start_row = 0
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        for n, row in enumerate(reader):
            if not data:
                if len(row) > 0 and row[0] == "IS":
                    row_len = len(row)
                    num_Vd = (row_len - 2) // 4
                    start_row = n + 1
                    data = True
                continue
            if len(row) != row_len:
                continue
            num_Vg += 1
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        Vg = np.zeros(num_Vg)
        Id = np.zeros((num_Vg, num_Vd))
        Ig = np.zeros((num_Vg, num_Vd))
        n_vg = 0
        for n, row in enumerate(reader):
            if n < start_row or len(row) != row_len:
                continue
            Vg[n_vg] = float(row[3 * num_Vd])
            for i in range(num_Vd):
                Ig[n_vg, i] = float(row[3 * num_Vd + 1 + i])
                Id[n_vg, i] = float(row[2 * num_Vd + i])
            n_vg += 1
        print(Id)
        ax[0, 0].semilogy(Vg, Id * 1e6 / 100, ".", color=colors[0])
        ax[0, 0].semilogy(Vg, Ig * 1e6 / 100, ".", color=colors[1])
        ax[0, 1].plot(Vg, Id * 1e6 / 100, ".", color=colors[0])
        # ax01t.plot(Vg[1:],(np.diff(Id, axis=0).T/np.diff(Vg)).T*1e6/100, '.', color=colors[1])
# ax[0].legend(legend)
# ax[1].legend(legend)
ax[0, 0].set_xlabel("Vgs [V]")
ax[0, 1].set_xlabel("Vgs [V]")
ax[0, 0].set_ylabel("Id,Ig [uA/um]")
ax[0, 1].set_ylabel("Id [uA/um]")
# ax01t.set_ylabel('gm [uA/um/V]')
# ax[0].set_ylim([1e-9, 1e-2])
# ax[1].set_ylim([1e-9, 1e-2])
# fig.tight_layout()
plt.show()
