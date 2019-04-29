import pandas as pd
import os


def to_csv(dataframe, filename):
    dataframe.to_csv(filename, mode="w", sep=";", encoding="latin1", index=False)


dirs = os.listdir(".")
for i, sub_dir in enumerate(dirs):
    if not os.path.isdir(sub_dir):
        continue
    if not "all_icd" in locals():
        all_icd = pd.read_csv(os.path.join(sub_dir, "ICD.csv"), delimiter=";",
                              na_filter=False, encoding="latin1", dtype=str)
        all_fall = pd.read_csv(os.path.join(sub_dir, "FALL.csv"), delimiter=";",
                               na_filter=False, encoding="latin1", dtype=str)
        all_entgelte = pd.read_csv(os.path.join(sub_dir, "Entgelte.csv"), delimiter=";",
                                   na_filter=False, encoding="latin1", dtype=str)
        all_fab = pd.read_csv(os.path.join(sub_dir, "FAB.csv"), delimiter=";",
                              na_filter=False, encoding="latin1", dtype=str)
        all_ops = pd.read_csv(os.path.join(sub_dir, "OPS.csv"), delimiter=";",
                              na_filter=False, encoding="latin1", dtype=str)
    else:
        all_icd.append(pd.read_csv(os.path.join(sub_dir, "ICD.csv"), delimiter=";",
                                   na_filter=False, encoding="latin1", dtype=str))
        all_fall.append(pd.read_csv(os.path.join(sub_dir, "FALL.csv"), delimiter=";",
                                    na_filter=False, encoding="latin1", dtype=str))
        all_entgelte.append(pd.read_csv(os.path.join(sub_dir, "Entgelte.csv"), delimiter=";",
                                        na_filter=False, encoding="latin1", dtype=str))
        all_fab.append(pd.read_csv(os.path.join(sub_dir, "FAB.csv"), delimiter=";",
                                   na_filter=False, encoding="latin1", dtype=str))
        all_ops.append(pd.read_csv(os.path.join(sub_dir, "OPS.csv"), delimiter=";",
                                   na_filter=False, encoding="latin1", dtype=str))

for name, csv in zip(["ICD.csv", "FALL.csv", "ENTGELTE.csv", "FAB.csv", "OPS.csv"],[all_icd, all_fall, all_entgelte, all_fab, all_ops]):
    to_csv(csv, name)
