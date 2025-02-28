import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "20250206/2_6_2025 10_45_31 AM;waferB_transistor_100_25_10_A1;62600 IdVd(3);.csv",
]

fig, ax = plt.subplots(1, 2)
legend = []
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        parsing_data = False
        Vd = []
        Id = []
        Ig = []
        for n, row in enumerate(reader):
            if parsing_data:
                if row[0] != "DataValue":
                    parsing_data = False
                    devname = fname.split(";")[1]
                    W = float(devname.split("_")[2])
                    ax[0].plot(Vd, np.array(Id) / W * 1e6)
                    ax[1].semilogy(Vd, np.array(Ig) / W * 1e6)
                    legend.append("_".join(devname.split("_")[2:]))
                    Vd = []
                    Id = []
                    Ig = []
                    break
                else:
                    Vd.append(float(row[1]))
                    Id.append(float(row[3]))
                    Ig.append(float(row[5]))
            else:
                if row[0] == "DataName":
                    parsing_data = True

# ax[0].legend(legend)
# ax[1].legend(legend)
ax[0].set_xlabel("Vds [V]")
ax[1].set_xlabel("Vds [V]")
ax[0].set_ylabel("Id [uA/um]")
ax[1].set_ylabel("Ig [uA/um]")
plt.show()
