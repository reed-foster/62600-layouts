import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    #'2_4_2025 11_27_09 AM;mim_50_20_A1;I_V Sweep(1);.csv',
    #'2_4_2025 11_31_11 AM;mim_70_20_A1;I_V Sweep(2);.csv',
    #'2_4_2025 11_31_39 AM;mim_80_20_A1;I_V Sweep(3);.csv',
    #'2_4_2025 11_32_40 AM;mim_100_20_A1;I_V Sweep(6);leakage seems to get worse gradually.csv',
    #'2_4_2025 11_33_38 AM;mim_100_40_A1;I_V Sweep(7);.csv',
    #'2_4_2025 11_34_06 AM;mim_50_40_A1;I_V Sweep(8);.csv',
    #'2_4_2025 11_34_48 AM;mim_50_200_A1;I_V Sweep(9);.csv',
    #'2_4_2025 11_35_10 AM;mim_50_200_A1;I_V Sweep(10);.csv',
    #'2_4_2025 11_35_38 AM;mim_100_200_A1;I_V Sweep(11);.csv',
    #'2_4_2025 11_36_23 AM;mos_50_200_A1;I_V Sweep(12);.csv',
    #'2_4_2025 11_39_52 AM;mos_70_200_A1;I_V Sweep(13);.csv',
    #'2_4_2025 11_40_23 AM;mos_80_200_A1;I_V Sweep(14);.csv',
    #'2_4_2025 11_40_48 AM;mos_100_200_A1;I_V Sweep(15);.csv',
    #'2_4_2025 11_41_29 AM;mos_100_80_A1;I_V Sweep(16);.csv',
    #'2_4_2025 11_41_54 AM;mos_80_80_A1;I_V Sweep(17);.csv',
    #'2_4_2025 11_42_15 AM;mos_70_80_A1;I_V Sweep(18);.csv',
    #'2_4_2025 11_43_55 AM;mos_50_80_A1;I_V Sweep(19);.csv',
    #'2_4_2025 11_44_36 AM;mos_50_20_A1;I_V Sweep(20);.csv',
    #'2_4_2025 11_45_04 AM;mos_50_20_A1;I_V Sweep(21);.csv',
    #'2_4_2025 11_45_31 AM;mos_70_20_A1;I_V Sweep(22);.csv',
    #'2_4_2025 11_45_58 AM;mos_80_20_A1;I_V Sweep(23);.csv',
    #'2_4_2025 11_46_26 AM;mos_100_20_A1;I_V Sweep(24);.csv',
    #'2_4_2025 11_47_50 AM;mos_50_20_C5;I_V Sweep(25);light on.csv',
    #'2_4_2025 11_48_12 AM;mos_50_20_C5;I_V Sweep(26);remeasure.csv',
    #'2_4_2025 11_48_45 AM;mos_70_20_C5;I_V Sweep(27);.csv',
    #'2_4_2025 11_49_06 AM;mos_80_20_C5;I_V Sweep(28);.csv',
    #'2_4_2025 11_49_29 AM;mos_100_20_C5;I_V Sweep(29);.csv',
    #'2_4_2025 11_50_20 AM;mos_100_80_C5;I_V Sweep(30);light on.csv',
    #'2_4_2025 11_50_37 AM;mos_100_80_C5;I_V Sweep(31);remeasure with light off.csv',
    #'2_4_2025 11_51_02 AM;mos_50_80_C5;I_V Sweep(32);.csv',
    #'2_4_2025 11_51_42 AM;mos_50_200_C5;I_V Sweep(33);.csv',
    #'2_4_2025 11_52_06 AM;mos_100_200_C5;I_V Sweep(34);.csv',
    #'2_4_2025 11_52_39 AM;mim_100_200_C5;I_V Sweep(35);.csv',
    #'2_4_2025 11_53_11 AM;mim_50_200_C5;I_V Sweep(36);.csv',
    #'2_4_2025 11_53_53 AM;mim_50_20_C5;I_V Sweep(37);.csv',
    #'2_4_2025 11_54_20 AM;mim_100_20_C5;I_V Sweep(38);.csv',
    #'2_4_2025 11_54_33 AM;mim_100_20_C5;I_V Sweep(39);remeasure.csv',
    #'2_4_2025 11_54_49 AM;mim_100_20_C5;I_V Sweep(40);.csv',
    #'2_4_2025 11_55_07 AM;mim_100_20_C5;I_V Sweep(41);.csv',
    #'2_4_2025 11_55_19 AM;mim_100_20_C5;I_V Sweep(42);.csv',
    #'2_4_2025 11_55_40 AM;mim_100_20_C5;I_V Sweep(43);.csv',
    #'2_4_2025 11_55_53 AM;mim_100_20_C5;I_V Sweep(44);IV curve keeps changing.csv',
    #'2_4_2025 11_56_45 AM;mos_100_20_A5;I_V Sweep(45);.csv',
    #'2_4_2025 11_56_59 AM;mos_100_20_A5;I_V Sweep(46);remeasure, pretty consistent.csv',
    #'2_4_2025 11_57_28 AM;mos_50_20_A5;I_V Sweep(47);.csv',
    #'2_4_2025 11_59_00 AM;mim_100_20_A5;I_V Sweep(54);IV curve very inconsistent.csv',
    #'2_4_2025 12_00_08 PM;mim_50_20_A5;I_V Sweep(58);inconsistent IV curve.csv',
    "2_4_2025 12_01_57 PM;mos_50_80_A5;I_V Sweep(66);leakage goes down with more cycles.csv",
    #'2_4_2025 12_03_08 PM;mos_100_80_A5;I_V Sweep(70);leakage goes down, but not as much as 50_80 device.csv',
    #'2_4_2025 12_03_55 PM;mos_100_200_A5;I_V Sweep(73);.csv',
    #'2_4_2025 12_04_42 PM;mos_50_200_A5;I_V Sweep(78);leakage goes up slightly.csv',
    #'2_4_2025 12_06_27 PM;mos_100_200_E5;I_V Sweep(80);.csv',
    #'2_4_2025 12_06_58 PM;mos_50_200_E5;I_V Sweep(82);.csv',
    #'2_4_2025 12_07_58 PM;mim_100_200_E5;I_V Sweep(86);leakage seems to go down with more measurements.csv',
    #'2_4_2025 12_09_10 PM;mim_50_200_E5;I_V Sweep(90);.csv',
    #'2_4_2025 12_09_49 PM;mos_100_80_E5;I_V Sweep(92);.csv',
    #'2_4_2025 12_10_24 PM;mos_50_80_E5;I_V Sweep(94);.csv',
    #'2_4_2025 12_11_27 PM;mim_100_80_E5;I_V Sweep(98);.csv',
    # "2_4_2025 12_12_42 PM;mim_50_80_E5;I_V Sweep(102);leakage didn't seem to decrease with trial number.csv",
    #'2_4_2025 12_13_33 PM;mos_100_20_E5;I_V Sweep(104);.csv',
    #'2_4_2025 12_14_00 PM;mos_50_20_E5;I_V Sweep(106);.csv',
    #'2_4_2025 12_15_05 PM;mim_100_20_E5;I_V Sweep(110);.csv',
    #'2_4_2025 12_16_12 PM;mim_50_20_E5;I_V Sweep(114);.csv',
    #'2_4_2025 12_17_27 PM;mos_100_20_E1;I_V Sweep(116);.csv',
    #'2_4_2025 12_18_56 PM;mos_50_20_E1;I_V Sweep(119);very low leakage (compared to other mos tests).csv',
    #'2_4_2025 12_20_04 PM;mim_100_20_E1;I_V Sweep(123);.csv',
    #'2_4_2025 12_20_59 PM;mim_50_20_E1;I_V Sweep(127);.csv',
    #'2_4_2025 12_22_38 PM;mos_50_80_E1;I_V Sweep(129);.csv',
    #'2_4_2025 12_23_09 PM;mos_100_80_E1;I_V Sweep(131);higher positive leakage.csv',
    #'2_4_2025 12_23_50 PM;mos_100_200_E1;I_V Sweep(133);.csv',
    #'2_4_2025 12_24_45 PM;mos_50_200_E1;I_V Sweep(139);.csv',
    #'2_4_2025 12_25_53 PM;mim_100_200_E1;I_V Sweep(143);.csv',
    #'2_4_2025 12_27_02 PM;mim_50_200_E1;I_V Sweep(147);.csv',
]

fig, ax = plt.subplots(3, 2)

V = [[] for _ in fnames]
I = [[] for _ in fnames]
areas = [[], []]
lengths = [[], []]
max_leak = [[], []]
legend = [[], []]
for f, fname in enumerate(fnames):
    # get L, W
    devname = fname.split(";")[1]
    W = float(devname.split("_")[1])
    L = float(devname.split("_")[2])
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        parsing_data = False
        for n, row in enumerate(reader):
            if parsing_data:
                if row[0] != "DataValue":
                    parsing_data = False
                    ax_idx = 1 if devname[:3] == "mos" else 0
                    # ax[0,ax_idx].semilogy(V[f], np.abs(I[f])/(W*L)*1e6)
                    ax[0, ax_idx].plot(V[f], np.array(I[f]) / (W * L) * 1e6)
                    legend[ax_idx].append("_".join(devname.split("_")[1:]))
                    leak = abs(np.array(I[f]))
                    leak[abs(np.array(V[f])) > 1] = 0
                    max_leak[ax_idx].append(np.max(leak))
                    areas[ax_idx].append(W * L)
                    lengths[ax_idx].append(2 * (W + L))
                    V[f] = []
                    I[f] = []
                else:
                    V[f].append(float(row[1]))
                    I[f].append(float(row[3]))
            else:
                if row[0] == "DataName":
                    parsing_data = True

# ax[0,0].legend(legend[0], ncols=2)
# ax[0,1].legend(legend[1], ncols=2)
ax[0, 0].set_xlabel("V [V]")
ax[0, 1].set_xlabel("V [V]")
ax[0, 0].set_ylabel("I [uA/um^2]")
ax[0, 1].set_ylabel("I [uA/um^2]")
for i in range(2):
    ax[1, i].scatter(np.array(areas[i]) / 1e6, np.array(max_leak[i]) * 1e6)
    ax[2, i].scatter(np.array(lengths[i]) / 1e3, np.array(max_leak[i]) * 1e6)
    ax[1, i].set_xlabel("area [mm^2]")
    ax[2, i].set_xlabel("perimeter [mm]")
    for j in range(2):
        ax[1 + j, i].set_ylabel("max leakage (|V|<4) [uA]")
        ax[1 + j, i].set_yscale("log")
        ax[1 + j, i].set_xscale("log")
# ax[0].set_ylim([1e-8, 1e1])
# ax[1].set_ylim([1e-8, 1e1])
plt.show()
