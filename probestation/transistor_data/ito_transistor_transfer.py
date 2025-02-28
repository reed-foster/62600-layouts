import csv
import numpy as np
import matplotlib.pyplot as plt

fnames = [
    #'20250130/1_30_2025 3_30_23 PM;transistor_100_25;62600 IdVg(4);.csv',
    #'20250130/1_30_2025 3_45_01 PM;transistor_100_10;62600 IdVg(1);.csv',
    #'20250130/1_30_2025 3_45_20 PM;transistor_100_10;62600 IdVg(2);.csv',
    #'20250130/1_30_2025 3_25_34 PM;transistor_30_25;62600 IdVg(1);.csv',
    #'20250130/1_30_2025 3_38_41 PM;transistor_100_3;62600 IdVg(5);BD in the middle.csv',
    #'20250130/1_30_2025 3_40_10 PM;transistor_100_5;62600 IdVg(7);.csv',
    #'20250130/1_30_2025 3_40_21 PM;transistor_100_5;62600 IdVg(8);again.csv',
    #'20250130/1_30_2025 3_41_30 PM;transistor_100_7;62600 IdVg(9);.csv',
    #'20250130/1_30_2025 3_41_52 PM;transistor_100_7;62600 IdVg(10);.csv',
    #'20250130/1_30_2025 3_42_08 PM;transistor_100_7;62600 IdVg(11);.csv',
    #'20250130/1_30_2025 3_47_01 PM;transistor_100_15;62600 IdVg(1);.csv',
    #'20250130/1_30_2025 3_47_15 PM;transistor_100_15;62600 IdVg(2);.csv',
    #'20250130/1_30_2025 3_49_46 PM;transistor_100_15_center;62600 IdVg(3);.csv',
    #'20250130/1_30_2025 3_51_34 PM;transistor_100_2_center;62600 IdVg(5);.csv',
    #'20250130/1_30_2025 3_52_57 PM;transistor_100_5_center;62600 IdVg(8);.csv',
    #'20250203/2_3_2025 11_26_05 AM;transistor_100_25_10_A1;62600 IdVg(2);.csv',
    #'20250203/2_3_2025 11_29_01 AM;transistor_100_25_5_A1;62600 IdVg(1);leaky.csv',
    #'20250203/2_3_2025 11_30_02 AM;transistor_100_25_2_A1;62600 IdVg(2);leaked to drain.csv',
    #'20250203/2_3_2025 11_31_08 AM;transistor_100_10_10_A1;62600 IdVg(3);.csv',
    #'20250203/2_3_2025 11_33_03 AM;transistor_100_10_5_A1;62600 IdVg(1);bd.csv',
    # "20250203/2_3_2025 11_34_16 AM;transistor_100_10_2_A1;62600 IdVg(2);doesn't shut off.csv",
    #'20250203/2_3_2025 11_37_10 AM;transistor_100_25_10_D5;62600 IdVg(3);bd (_).csv',
    #'20250203/2_3_2025 11_37_52 AM;transistor_100_25_10_D5;62600 IdVg(4);bd _.csv',
    #'20250203/2_3_2025 11_38_48 AM;transistor_100_25_5_D5;62600 IdVg(5);leaky.csv',
    #'20250203/2_3_2025 11_39_28 AM;transistor_100_25_2_D5;62600 IdVg(6);leaky.csv',
    #'20250203/2_3_2025 11_41_10 AM;transistor_100_25_10_D1;62600 IdVg(7);good.csv',
    #'20250203/2_3_2025 11_43_17 AM;transistor_100_25_5_D1;62600 IdVg(1);leaky.csv',
    #'20250203/2_3_2025 11_44_03 AM;transistor_100_25_2_D1;62600 IdVg(2);no field effect.csv',
    #'20250203/2_3_2025 11_46_54 AM;transistor_100_25_10_E1;62600 IdVg(4);leaky.csv',
    #'20250203/2_3_2025 11_47_39 AM;transistor_100_25_5_E1;62600 IdVg(5);less leaky.csv',
    #'20250203/2_3_2025 11_50_01 AM;transistor_100_25_2_E1;62600 IdVg(7);turns off fairly well.csv',
    #'20250203/2_3_2025 11_51_44 AM;transistor_100_25_10_E5;62600 IdVg(9);very leaky.csv',
    #'20250203/2_3_2025 11_52_35 AM;transistor_100_25_5_E5;62600 IdVg(10);bd.csv',
    #'20250203/2_3_2025 11_53_48 AM;transistor_100_25_2_E5;62600 IdVg(12);leaky.csv',
    #'20250203/2_3_2025 11_55_43 AM;transistor_100_25_10_A5;62600 IdVg(13);leaky.csv',
    #'20250203/2_3_2025 11_56_21 AM;transistor_100_25_5_A5;62600 IdVg(14);leaky.csv',
    #'20250203/2_3_2025 11_57_17 AM;transistor_100_25_2_A5;62600 IdVg(15);leaky.csv',
    #'20250203/2_3_2025 11_58_14 AM;transistor_100_10_2_A5;62600 IdVg(16);no field effect.csv',
    #'20250203/2_3_2025 11_59_07 AM;transistor_100_10_5_A5;62600 IdVg(17);no field.csv',
    #'20250203/2_3_2025 11_59_48 AM;transistor_100_10_10_A5;62600 IdVg(18);no field effect.csv',
    #'20250203/2_3_2025 12_01_25 PM;transistor_100_25_10_A10;62600 IdVg(19);huge leakage.csv',
    #'20250203/2_3_2025 12_02_17 PM;transistor_100_25_5_A10;62600 IdVg(20);actual breakdown.csv',
    #'20250203/2_3_2025 12_04_08 PM;transistor_100_25_10_B3;62600 IdVg(21);leakage.csv',
    #'20250203/2_3_2025 12_05_03 PM;transistor_100_25_10_C3;62600 IdVg(22);breakdown.csv',
    #'20250203/2_3_2025 12_13_56 PM;transistor_100_25_5_C3;62600 IdVg(23);pretty low leakage.csv',
    #'20250203/2_3_2025 12_15_18 PM;transistor_100_25_2_C3;62600 IdVg(24);high leakage.csv',
    #'20250203/2_3_2025 12_17_29 PM;transistor_100_25_10_C10;62600 IdVg(25);no field effect.csv',
    #'20250203/2_3_2025 12_18_13 PM;transistor_100_25_5_C10;62600 IdVg(26);high leakage.csv',
    #'20250203/2_3_2025 12_18_50 PM;transistor_100_25_2_C10;62600 IdVg(27);high leakage.csv',
    #'20250203/2_3_2025 12_20_04 PM;transistor_100_25_10_B7;62600 IdVg(28);high leakage.csv',
    #'20250203/2_3_2025 12_21_30 PM;transistor_100_25_5_B7;62600 IdVg(29);high leakage.csv',
    #'20250203/2_3_2025 12_23_03 PM;transistor_100_25_10_E10;62600 IdVg(30);no field effect.csv',
    #'20250203/2_3_2025 12_23_43 PM;transistor_100_25_5_E10;62600 IdVg(31);no field effect.csv',
    #'20250203/2_3_2025 12_24_41 PM;transistor_100_10_10_E10;62600 IdVg(32);high leakage.csv',
    #'20250203/2_3_2025 12_26_32 PM;transistor_100_5_10_E10;62600 IdVg(33);no field effect.csv',
    #'20250203/2_3_2025 12_28_47 PM;transistor_100_25_10_B1;62600 IdVg(34);very low leakage.csv',
    #'20250203/2_3_2025 12_30_00 PM;transistor_100_25_5_B1;62600 IdVg(35);high leakage _ no field effect.csv',
    #'20250203/2_3_2025 12_31_14 PM;transistor_100_25_2_B1;62600 IdVg(37);high leakage _ no field effect.csv',
    #'20250203/2_3_2025 12_32_04 PM;transistor_100_10_2_B1;62600 IdVg(38);very low leakage.csv',
    #'20250203/2_3_2025 12_33_07 PM;transistor_100_10_5_B1;62600 IdVg(39);no field effect.csv',
    #'20250203/2_3_2025 12_33_45 PM;transistor_100_10_10_B1;62600 IdVg(40);low leakage.csv',
    #'20250203/2_3_2025 12_39_20 PM;transistor_100_25_10_D8;62600 IdVg(41);leakage.csv',
    #'20250203/2_3_2025 12_40_01 PM;transistor_100_25_5_D8;62600 IdVg(42);leakage _ no fe.csv',
    #'20250203/2_3_2025 12_40_35 PM;transistor_100_25_2_D8;62600 IdVg(43);leakage.csv',
    #'20250203/2_3_2025 12_41_30 PM;transistor_100_10_2_D8;62600 IdVg(44);disconnected_.csv',
    #'20250203/2_3_2025 12_43_01 PM;transistor_100_10_2_D8;62600 IdVg(46);very low leakage.csv',
    #'20250203/2_3_2025 12_43_49 PM;transistor_100_10_5_D8;62600 IdVg(47);high leakage.csv',
    #'20250203/2_3_2025 12_44_27 PM;transistor_100_10_10_D8;62600 IdVg(48);lowish leakage.csv',
    #'20250203/2_3_2025 12_46_03 PM;transistor_100_25_10_A8;62600 IdVg(49);leakage.csv',
    #'20250203/2_3_2025 12_46_38 PM;transistor_100_25_5_A8;62600 IdVg(50);high leakage.csv',
    #'20250203/2_3_2025 12_47_12 PM;transistor_100_25_2_A8;62600 IdVg(51);very high leakage.csv',
    #'20250203/2_3_2025 12_47_58 PM;transistor_100_10_2_A8;62600 IdVg(52);leakage.csv',
    #'20250203/2_3_2025 12_48_55 PM;transistor_100_10_5_A8;62600 IdVg(53);leakage.csv',
    #'20250203/2_3_2025 12_49_25 PM;transistor_100_10_10_A8;62600 IdVg(54);high leakage.csv',
    #'20250203/2_3_2025 12_51_57 PM;transistor_100_25_10_A2;62600 IdVg(55);high leakage.csv',
    #'20250203/2_3_2025 12_53_04 PM;transistor_100_25_5_A2;62600 IdVg(56);lower leakage.csv',
    #'20250203/2_3_2025 12_53_58 PM;transistor_100_25_2_A2;62600 IdVg(57);__.csv',
    #'20250203/2_3_2025 12_54_45 PM;transistor_100_25_2_A2;62600 IdVg(58);reprobed, high leakage.csv',
    #'20250203/2_3_2025 12_55_46 PM;transistor_100_10_2_A2;62600 IdVg(59);high leakage.csv',
    #'20250203/2_3_2025 12_56_43 PM;transistor_100_10_5_A2;62600 IdVg(60);high leakage.csv',
    #'20250203/2_3_2025 12_57_19 PM;transistor_100_10_10_A2;62600 IdVg(61);lower leakage.csv',
    #'20250203/2_3_2025 12_59_28 PM;transistor_100_25_10_E3;62600 IdVg(62);lower leakage.csv',
    #'20250203/2_3_2025 1_00_06 PM;transistor_100_25_5_E3;62600 IdVg(63);high leakage.csv',
    #'20250203/2_3_2025 1_00_38 PM;transistor_100_25_2_E3;62600 IdVg(64);high leakage.csv',
    #'20250203/2_3_2025 1_01_21 PM;transistor_100_10_2_E3;62600 IdVg(65);lower leakage.csv',
    #'20250203/2_3_2025 1_02_14 PM;transistor_100_10_5_E3;62600 IdVg(66);lower leakage.csv',
    #'20250203/2_3_2025 1_02_45 PM;transistor_100_10_5_E3;62600 IdVg(67);lower leakage, remeasure.csv',
    #'20250203/2_3_2025 1_04_46 PM;transistor_100_10_10_E3;62600 IdVg(68);lower leakage.csv',
    #'20250203/2_3_2025 1_07_17 PM;transistor_100_25_10_B7;62600 IdVg(69);small jump in Ig for prev measurement might be breakdown.csv',
    #'20250203/2_3_2025 1_08_46 PM;transistor_100_15_10_B7;62600 IdVg(70);lowish leakage.csv',
    #'20250203/2_3_2025 1_10_09 PM;transistor_100_25_10_B5;62600 IdVg(71);lower leakage.csv',
    #'20250203/2_3_2025 1_10_36 PM;transistor_100_25_10_B5;62600 IdVg(72);maybe some oxide damage, compare with prev measurement.csv',
    #'20250203/2_3_2025 1_11_27 PM;transistor_100_10_10_B5;62600 IdVg(73);lowish leakage.csv',
    #'20250203/2_3_2025 1_12_09 PM;transistor_100_25_5_B5;62600 IdVg(74);highish leakage.csv',
    #'20250203/2_3_2025 1_12_50 PM;transistor_100_25_2_B5;62600 IdVg(75);high leakage.csv',
    #'20250203/2_3_2025 1_13_40 PM;transistor_100_10_2_B5;62600 IdVg(76);high leakage.csv',
    #'20250203/2_3_2025 1_14_02 PM;transistor_100_10_2_B5;62600 IdVg(77);high leakage, repeat of measurement.csv',
    #'20250203/2_3_2025 1_14_57 PM;transistor_100_25_10_C5;62600 IdVg(78);high leakage.csv',
    #'20250203/2_3_2025 1_16_56 PM;transistor_100_25_10_C6;62600 IdVg(79);leakage.csv',
    #'20250203/2_3_2025 1_17_36 PM;transistor_100_10_10_C6;62600 IdVg(80);.csv',
    #'20250203/2_3_2025 1_18_22 PM;transistor_100_10_5_C6;62600 IdVg(81);bad contact_.csv',
    #'20250203/2_3_2025 1_19_38 PM;transistor_100_10_5_C6;62600 IdVg(82);better contact, high leakage.csv',
    #'20250203/2_3_2025 1_20_15 PM;transistor_100_10_2_C6;62600 IdVg(83);low leakage.csv',
    #'20250203/2_3_2025 1_20_51 PM;transistor_100_25_2_C6;62600 IdVg(84);lower leakage.csv',
    #'20250203/2_3_2025 1_21_27 PM;transistor_100_25_5_C6;62600 IdVg(85);bad contact_ jump in Ig_.csv',
    #'20250203/2_3_2025 1_22_21 PM;transistor_100_25_5_C6;62600 IdVg(86);better contact, jump is missing.csv',
    #'20250203/2_3_2025 1_23_45 PM;transistor_100_25_10_C1;62600 IdVg(87);jump in Ig.csv',
    #'20250203/2_3_2025 1_24_12 PM;transistor_100_25_10_C1;62600 IdVg(88);jump is gone.csv',
    #'20250203/2_3_2025 1_25_13 PM;transistor_100_25_5_C1;62600 IdVg(89);bad source contact_.csv',
    # "20250203/2_3_2025 1_26_08 PM;transistor_100_25_5_C1;62600 IdVg(90);no, device just doesn't work.csv",
    #'20250203/2_3_2025 1_26_55 PM;transistor_100_25_2_C1;62600 IdVg(91);lowish leakage.csv',
    #'20250203/2_3_2025 1_27_45 PM;transistor_100_10_2_C1;62600 IdVg(92);very low leakage.csv',
    #'20250203/2_3_2025 1_28_34 PM;transistor_100_10_5_C1;62600 IdVg(93);.csv',
    #'20250203/2_3_2025 1_29_08 PM;transistor_100_10_5_C1;62600 IdVg(94);some sort of breakdown occurred, compare with prev measurement.csv',
    #'20250203/2_3_2025 1_29_47 PM;transistor_100_10_10_C1;62600 IdVg(95);jump in Ig.csv',
    #'20250203/2_3_2025 1_30_07 PM;transistor_100_10_10_C1;62600 IdVg(96);jump is gone.csv',
    "20250206/2_6_2025 10_03_32 AM;waferB_transistor_100_25_10_A1;62600 IdVg(1);.csv",
    #'20250206/2_6_2025 10_11_27 AM;waferB_transistor_100_25_10_C5;62600 IdVg(4);.csv',
    #'20250206/2_6_2025 10_14_56 AM;waferB_transistor_100_25_10_E2;62600 IdVg(7);.csv',
    #'20250206/2_6_2025 10_18_16 AM;waferB_transistor_100_25_10_E10;62600 IdVg(10);.csv',
    #'20250206/2_6_2025 10_22_21 AM;waferB_transistor_100_25_10_B9;62600 IdVg(12);.csv',
    #'20250206/2_6_2025 10_23_31 AM;waferB_transistor_100_25_10_B8;62600 IdVg(14);.csv',
    #'20250206/2_6_2025 10_25_53 AM;waferB_transistor_100_25_5_A1;62600 IdVg(16);.csv',
    #'20250206/2_6_2025 10_27_40 AM;waferB_transistor_100_25_5_C5;62600 IdVg(18);.csv',
    #'20250206/2_6_2025 10_29_20 AM;waferB_transistor_100_25_5_B3;62600 IdVg(20);.csv',
    #'20250206/2_6_2025 10_30_25 AM;waferB_transistor_100_25_10_B3;62600 IdVg(22);.csv',
    #'20250206/2_6_2025 10_32_23 AM;waferB_transistor_100_25_10_B2;62600 IdVg(24);.csv',
    #'20250206/2_6_2025 10_34_04 AM;waferB_transistor_100_25_5_B2;62600 IdVg(27);.csv',
    #'20250206/2_6_2025 10_35_21 AM;waferB_transistor_100_25_10_B1;62600 IdVg(29);.csv',
    #'20250206/2_6_2025 10_36_22 AM;waferB_transistor_100_25_5_B1;62600 IdVg(31);.csv',
    #'20250206/2_6_2025 10_37_53 AM;waferB_transistor_100_25_5_A2;62600 IdVg(33);.csv',
    #'20250206/2_6_2025 10_39_03 AM;waferB_transistor_100_25_10_A2;62600 IdVg(35);.csv',
]

fig, ax = plt.subplots(1, 2)
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
        for n, row in enumerate(reader):
            if parsing_data:
                if row[0] != "DataValue" or (n == n_max - 1):
                    parsing_data = False
                    devname = fname.split(";")[1]
                    W = float(devname.split("_")[2])
                    ax[0].semilogy(Vg, np.array(Id) / W * 1e6)
                    ax[1].plot(Vg, np.array(Id) / W * 1e6)
                    # ax[0].plot(Vg, np.array(Id)/W*1e6)
                    # ax[1].semilogy(Vg, np.array(Ig)/W*1e6)
                    legend.append("_".join(devname.split("_")[2:]))
                    print(
                        f"{devname}: Ig,max = %s" % float("%.2g" % np.max(np.abs(Ig)))
                    )
                    Vg = []
                    Id = []
                    Ig = []
                else:
                    Vg.append(float(row[1]))
                    Id.append(float(row[3]))
                    Ig.append(float(row[5]))
            else:
                if row[0] == "DataName":
                    parsing_data = True

# ax[0].legend(legend)
# ax[1].legend(legend)
ax[0].set_xlabel("Vgs [V]")
ax[1].set_xlabel("Vgs [V]")
ax[0].set_ylabel("Id [uA/um]")
ax[1].set_ylabel("Ig [uA/um]")
ax[0].set_ylim([1e-9, 1e-2])
ax[1].set_ylim([1e-9, 1e-2])
plt.show()
