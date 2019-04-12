import pandas as pd
import sys 
import chardet
import time


start = time.time()
change = sys.argv[-1]
mode=""
if "%" in change:	
	try:
   		change=int(change.replace("%","").strip())
   		mode="percent"
   		print("Die Beatmungsstunden werden um {} erhöht".format(change))
	except ValueError:
   		print("{} ist keine gültige Zahl.".format(change))
	
else:
	try:
   		change=int(change.strip())
   		mode="absolut"
   		print("Die Beatmungsstunden werden um {} Stunden erhöht.".format(change))
	except ValueError:
   		print("{} ist keine gültige Zahl.".format(change))

with open("Fall.csv", 'rb') as f:
	enco = chardet.detect(f.read(1024 ** 2))
print(" Das Encoding der Fall-Datei wird als {} angenommen.".format(enco["encoding"]))


fall= pd.read_csv("Fall.csv",encoding=enco["encoding"],sep=";",na_filter=False,dtype=str)
fall = fall[fall["Beatmungsstunden"]!=""]
try:
	fall["Beatmungsstunden"] = fall["Beatmungsstunden"].astype(int)
except ValueError:
	print("Beatmungsstunden können nicht als Zahl eingelesen werden. Enthält die Spalte in der Fall-Datei leere Felder?")
	sys.exit(1)

if mode == "absolut":
	fall["Beatmungsstunden"] = fall["Beatmungsstunden"].apply(lambda x: str(x+change).zfill(4))
if mode == "percent":
	fall["Beatmungsstunden"] = fall["Beatmungsstunden"].apply(lambda x: str(x*(1+change/100).zfill(4)))

fall.to_csv("Fall_{}.csv".format(sys.argv[-1]),encoding=enco["encoding"],sep=";",index=False)
now= int(time.time() - start)
print("Das Modifizieren hat {} sek. gedauert.".format(now))
