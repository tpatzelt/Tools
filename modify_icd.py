import pandas as pd
import sys 
import chardet
import time


start = time.time()
icd_kode = sys.argv[-1]
icd_kode = icd_kode.split(";")
icd_kode = [str(_icd_kode).strip() for _icd_kode in icd_kode]
print(" Der ICD-Kode {} wird zur ICD-Datei hinzugefügt".format(icd_kode))
with open("ICD.csv", 'rb') as f:
	enco = chardet.detect(f.read(1024 ** 2))
print(" Das Encoding der ICD-Datei wird als {} angenommen.".format(enco["encoding"]))

icd= pd.read_csv("ICD.csv",encoding=enco["encoding"],sep=";",na_filter=False,dtype=str)
to_append = list()
for id,group in icd.groupby("KH-internes-Kennzeichen"):
	for _icd_kode in icd_kode:
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
		d["ICD-Kode"] = _icd_kode
		to_append.append(d)

#for patid in icd["KH-internes-Kennzeichen"].unique():
icd = icd.append(pd.DataFrame(to_append, columns=icd.columns))

icd.to_csv("ICD_{}.csv".format("_".join(icd_kode)),encoding=enco["encoding"],sep=";",index=False)
now= int(time.time() - start)
print("Das Modifizieren hat {} sek. gedauert.".format(now))
