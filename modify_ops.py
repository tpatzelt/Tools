import pandas as pd
import sys 
import chardet
import time


start = time.time()
ops_kode = sys.argv[-1]
print(" Der OPS-Kode {} wird zur OPS-Datei hinzugefügt".format(ops_kode))
with open("OPS.csv", 'rb') as f:
	enco = chardet.detect(f.read(1024 ** 2))
print(" Das Encoding der OPS-Datei wird als {} angenommen.".format(enco["encoding"]))

ops= pd.read_csv("OPS.csv",encoding=enco["encoding"],sep=";",na_filter=False,dtype=str)
to_append = list()
for id,group in ops.groupby("KH-internes-Kennzeichen"):
	d=dict()
	ops_row = group.iloc[0,:].copy()
	d["IK"] = ops_row["IK"]
	d["Entlassender-Standort"] = ops_row["Entlassender-Standort"]
	d["Entgeltbereich"] = ops_row["Entgeltbereich"]
	d["KH-internes-Kennzeichen"] = ops_row["KH-internes-Kennzeichen"]
	d["OPS-Version"] = ops_row["OPS-Version"]
	d["Lokalisation"] = ""
	d["OPS-Datum"] = ops_row["OPS-Datum"]
	d["Belegoperateur"] = ""
	d["Beleganästhesist"]="ND"
	d["Beleghebamme"] = ""
	d["OPS-Kode"] = ops_kode
	to_append.append(d)

#for patid in ops["KH-internes-Kennzeichen"].unique():
ops = ops.append(pd.DataFrame(to_append, columns=ops.columns))

ops.to_csv("OPS_{}.csv".format(ops_kode),encoding=enco["encoding"],sep=";",index=False)
now= int(time.time() - start)
print("Das Modifizieren hat {} sek. gedauert.".format(now))
