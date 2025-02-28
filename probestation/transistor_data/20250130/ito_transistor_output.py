import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    #'1_30_2025 3_32_07 PM;transistor_100_25;62600 IdVd(2);.csv',
    #'1_30_2025 3_46_24 PM;transistor_100_10;62600 IdVd(1);.csv',
    "1_30_2025 3_20_07 PM;transistor_30_2;62600 IdVd(10);.csv",
    #'1_30_2025 3_43_32 PM;transistor_100_7;62600 IdVd(1);.csv',
    #'1_30_2025 3_53_49 PM;transistor_100_5_center;62600 IdVd(1);.csv',
]

fig, ax = plt.subplots(1, 2)

Vd = [[] for _ in fnames]
Id = [[] for _ in fnames]
Ig = [[] for _ in fnames]
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        for n, row in enumerate(reader):
            if n < 122:
                continue
            Vd[f].append(float(row[0]))
            Id[f].append(float(row[1]))
            Ig[f].append(float(row[2]))

    ax[0].plot(Vd[f], 1e6 * np.array(Id[f]))
    ax[1].semilogy(Vd[f], Ig[f])

ax[0].legend(["_".join(s.split(";")[1].split("_")[1:]) for s in fnames])
ax[0].set_xlabel("Vds [V]")
ax[1].set_xlabel("Vds [V]")
ax[0].set_ylabel("Id [uA]")
ax[1].set_ylabel("Ig [A]")
plt.show()
