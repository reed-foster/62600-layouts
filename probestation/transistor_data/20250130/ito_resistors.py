import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    "1_30_2025 3_01_57 PM;ITO_10_2;I_V Sweep(3);.csv",
    "1_30_2025 3_03_37 PM;ITO_20_2;I_V Sweep(1);.csv",
    "1_30_2025 3_04_31 PM;ITO_20_10;I_V Sweep(2);.csv",
    "1_30_2025 3_05_10 PM;ITO_10_10;I_V Sweep(3);.csv",
    "1_30_2025 3_05_43 PM;ITO_10_25;I_V Sweep(4);.csv",
    "1_30_2025 3_06_33 PM;ITO_10_15;I_V Sweep(5);.csv",
]
V = [[] for _ in fnames]
I = [[] for _ in fnames]
R = []
squares = []
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
    size = fname.split(";")[1].split("_")[1:]
    squares.append(float(size[1]) / float(size[0]))
    R.append(b[1])
    print(
        f"R^2 = {1 - sum((b[0]+b[1]*xi - yi)**2 for xi,yi in zip(I[f],V[f]))/sum((yi-np.mean(y))**2 for yi in V[f])}"
    )

    plt.plot(1e6 * np.array(I[f]), V[f])
plt.xlabel("I [uA]")
plt.ylabel("V [V]")
plt.legend([s.split(";")[1] for s in fnames])
plt.show()

X = np.ones((len(squares), 2))
X[:, 1] = np.array(squares)
y = np.array(R)
b, residuals, _, _ = np.linalg.lstsq(X, y)
sq = np.linspace(0, np.max(squares), 100)
plt.plot(squares, 1e-3 * np.array(R), "o")
plt.plot(sq, 1e-3 * (b[0] + b[1] * sq))
plt.legend(
    ["data", f"fit: Rc = {round(b[0]/1e3/2)}kOhm, Rsheet = {round(b[1]/1e3)}kOhm"]
)
plt.xlabel("squares")
plt.ylabel("R [kOhm]")
plt.show()
