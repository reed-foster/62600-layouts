import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    # "wafer_G/wafer_G_A1_transistor_100_2_2.dat",
    # "wafer_T/wafer_T_A1_transistor_100_1_5.dat",
    # "wafer_T/wafer_T_A1_transistor_100_2_2.dat",
    "wafer_T/wafer_T_G4_transistor_100_20_5.dat",
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
legend = []


def get_curve_size(fname):
    data = False
    num_transfer_Vg = 0
    num_transfer_Vd = 0
    num_output_Vg = 0
    num_output_Vd = 0
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        for n, row in enumerate(reader):
            if not data:
                if len(row) > 0 and row[0] == "IS":
                    num_transfer_Vd = (len(row) - 2) // 4
                    data = True
                continue
            if len(row) == 0:
                break
            num_transfer_Vg += 1
        data = False
        for n, row in enumerate(reader):
            if not data:
                if len(row) > 0 and row[0] == "IS":
                    num_output_Vg = (len(row) - 2) // 4
                    data = True
                continue
            if len(row) == 0:
                break
            num_output_Vd += 1
    return num_transfer_Vg, num_transfer_Vd, num_output_Vg, num_output_Vd


for f, fname in enumerate(fnames):
    num_transfer_Vg, num_transfer_Vd, num_output_Vg, num_output_Vd = get_curve_size(
        fname
    )
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        Vg = np.zeros(num_transfer_Vg)
        Id = np.zeros((num_transfer_Vg, num_transfer_Vd))
        Ig = np.zeros((num_transfer_Vg, num_transfer_Vd))
        n_vg = 0
        for n, row in enumerate(reader):
            if len(row) != num_transfer_Vd * 4 + 2:
                if n_vg == 0:
                    continue
                break
            if row[0] == "IS":
                continue
            Vg[n_vg] = float(row[3 * num_transfer_Vd])
            for i in range(num_transfer_Vd):
                Ig[n_vg, i] = float(row[3 * num_transfer_Vd + 1 + i])
                Id[n_vg, i] = float(row[2 * num_transfer_Vd + i])
            n_vg += 1
        ax[0, 0].semilogy(Vg, Id * 1e6 / 100, ".", color=colors[0])
        ax[0, 0].semilogy(Vg, Ig * 1e6 / 100, ".", color=colors[1])
        ax[0, 1].plot(Vg, Id * 1e6 / 100, ".", color=colors[0])
        ax[1, 1].plot(
            Vg[1:],
            (np.diff(Id, axis=0).T / np.diff(Vg)).T * 1e6 / 100,
            ".",
            color=colors[1],
        )
        Vd = np.zeros(num_output_Vd)
        Id = np.zeros((num_output_Vd, num_output_Vg))
        Ig = np.zeros((num_output_Vd, num_output_Vg))
        n_vd = 0
        for n, row in enumerate(reader):
            if len(row) != num_output_Vg * 4 + 2:
                if n_vd == 0:
                    continue
                break
            if row[0] == "IS":
                continue
            Vd[n_vd] = float(row[num_output_Vg])
            for i in range(num_output_Vg):
                Ig[n_vd, i] = float(row[3 * num_output_Vg + 1 + i])
                Id[n_vd, i] = float(row[num_output_Vg + 1 + i])
            n_vd += 1
        ax[1, 0].plot(Vd, Id * 1e6 / 100, ".", color=colors[0])

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
# ax[0].set_ylim([1e-9, 1e-2])
# ax[1].set_ylim([1e-9, 1e-2])
# fig.tight_layout()
plt.show()
