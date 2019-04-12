import pandas as pd
import sys 
import chardet
import time
import os


start = time.time()
P21_OUTPUT = "./P21 modifiziert/"
if not os.path.exists(P21_OUTPUT):
	os.makedirs(P21_OUTPUT)

fallnummer_listen = sys.argv[-1]
fallnummern = pd.read_csv(fallnummer_listen,encoding="latin1",sep=";",na_filter=False,dtype=str)

with open("Fall.csv", 'rb') as f:
	enco = chardet.detect(f.read(1024 ** 2))
print(" Das Encoding der P21-Dateien wird als {} angenommen.".format(enco["encoding"]))

all_icd = pd.read_csv("ICD.csv", delimiter=";", na_filter = False,encoding=enco["encoding"],dtype=str)
all_fall = pd.read_csv("Fall.csv", delimiter=";", na_filter = False,encoding=enco["encoding"],dtype=str)
all_fab = pd.read_csv("FAB.csv", delimiter=";", na_filter = False,encoding=enco["encoding"],dtype=str)
all_ops = pd.read_csv("OPS.csv", delimiter=";", na_filter = False,encoding=enco["encoding"],dtype=str)

for col in fallnummern.columns:
	keep_ids = fallnummern[col]
	column = col.strip()
	icd = all_icd[all_icd["KH-internes-Kennzeichen"].isin(keep_ids)]
	fall = all_fall[all_fall["KH-internes-Kennzeichen"].isin(keep_ids)]
	fab = all_fab[all_fab["KH-internes-Kennzeichen"].isin(keep_ids)]
	ops = all_ops[all_ops["KH-internes-Kennzeichen"].isin(keep_ids)]


	to_append = list()
	for id,group in icd.groupby("KH-internes-Kennzeichen"):
		d=dict()
		icd_row = group.iloc[0,:].copy()
		d["IK"] = icd_row["IK"]
		d["Entlassender-Standort"] = icd_row["Entlassender-Standort"]
		d["Entgeltbereich"] = icd_row["Entgeltbereich"]
		d["KH-internes-Kennzeichen"] = icd_row["KH-internes-Kennzeichen"]
		d["ICD-Version"] = icd_row["ICD-Version"]
		d["Diagnosensicherheit"] = ""
		d["Diagnosensicherheit.1"] = ""
		d["Diagnoseart"]="ND"
		d["Sekundär-Kode"] = ""
		d["Lokalisation"] = ""
		d["Lokalisation.1"] = ""
		d["ICD-Kode"] = column
		to_append.append(d)
	
	#for patid in icd["KH-internes-Kennzeichen"].unique():
	icd = icd.append(pd.DataFrame(to_append, columns=icd.columns))
	P21_OUTPUT_SINGLE = P21_OUTPUT + "P21_{}".format(column)
	if not os.path.exists(P21_OUTPUT_SINGLE):
		os.makedirs(P21_OUTPUT_SINGLE)
	
	icd.to_csv(P21_OUTPUT_SINGLE+"/ICD.csv",encoding=enco["encoding"],sep=";",index=False)
	fall.to_csv(P21_OUTPUT_SINGLE+"/Fall.csv",encoding=enco["encoding"],sep=";",index=False)
	fab.to_csv(P21_OUTPUT_SINGLE+"/FAB.csv",encoding=enco["encoding"],sep=";",index=False)
	ops.to_csv(P21_OUTPUT_SINGLE+"/OPS.csv",encoding=enco["encoding"],sep=";",index=False)



now= int(time.time() - start)
print("Das Modifizieren hat {} sek. gedauert.".format(now))
	