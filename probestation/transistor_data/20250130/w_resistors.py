import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "1_30_2025 2_59_37 PM;W2_100;I_V Sweep(2);.csv",
    "1_30_2025 2_55_45 PM;W1_100;I_V Sweep(1);.csv",
]
V = [[] for _ in fnames]
I = [[] for _ in fnames]
for f, fname in enumerate(fnames):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        for n, row in enumerate(reader):
            if n < 114:
                continue
            V[f].append(float(row[0]))
            I[f].append(float(row[1]))

    X = np.ones((len(V[f]), 2))
    X[:, 1] = np.array(I[f])
    y = np.array(V[f])
    b, residuals, _, _ = np.linalg.lstsq(X, y)

    print(fname)
    print(f"Rsheet = {b[1]/101}, rho = {b[1]/101*30e-9}")
    print(
        f"R^2 = {1 - sum((b[0]+b[1]*xi - yi)**2 for xi,yi in zip(I[f],V[f]))/sum((yi-np.mean(y))**2 for yi in V[f])}"
    )

    plt.plot(1e3 * np.array(I[f]), V[f])
plt.xlabel("I [mA]")
plt.ylabel("V [V]")
plt.legend([s.split(";")[1] for s in fnames])
plt.show()
