import pandas as pd
import os
import datetime
from dateutil.parser import parse

FALLDatei = "FALL.csv"
ENTGELTEDatei = "ENTGELTE.csv"
ICDDatei = "ICD.csv"
OPSDatei = "OPS.csv"
FABDatei = "FAB.csv"

GrouperDateien = [FALLDatei,ENTGELTEDatei,ICDDatei,OPSDatei,FABDatei]

FALL = pd.read_csv(FALLDatei,encoding="latin1",delimiter=";",na_filter=False,dtype=str)
orig_fälle = len(FALL)
print("originale FALLdatei enthielt: {} Fälle.".format(orig_fälle))
FALL = FALL[~FALL["Aufnahmegrund"].str.match(r"0?3[0-9][0-9].*")]
print("Keine Fälle mit 03XX als Aufnahmegrund:",len(FALL),"(-{} Fälle)".format(orig_fälle-len(FALL)))
orig_fälle = len(FALL)
FALL = FALL[~FALL["Aufnahmegrund"].str.match(r"0?4[0-9][0-9].*")]
print("Keine Fälle mit 04XX als Aufnahmegrund:",len(FALL),"(-{} Fälle)".format(orig_fälle-len(FALL)))
orig_fälle = len(FALL)
FALL = FALL[FALL["Aufnahmegrund"] != ""]
print("Keine Fälle mit leerem Aufnahmegrund:",len(FALL),"(-{} Fälle)".format(orig_fälle-len(FALL)))
orig_fälle = len(FALL)
FALL = FALL[FALL["Aufnahmedatum"].str.startswith("2017")]
print("Nur Fälle mit Aufnahmedatum 2017: ",len(FALL),"(-{} Fälle)".format(orig_fälle-len(FALL)))
orig_fälle = len(FALL)
FALL = FALL[FALL["Entgeltbereich"] == "DRG"]
print("Nur Fälle mit DRG-Entgeltbereich: ",len(FALL),"(-{} Fälle)".format(orig_fälle-len(FALL)))
#orig_fälle = len(FALL)
#FALL["Aufnahmedatum"].apply(lambda x: datetime.datetime.strptime(x,"%Y%m%d%H%M"))
#FALL["Entlassungsdatum"].apply(lambda x: datetime.datetime.strptime(x,"%Y%m%d%H%M"))
#FALL["Aufenthaltszeit in Stunden"] = (((FALL["Aufnahmedatum"] - FALL["Entlassungsdatum"]).apply(lambda x: x.total_seconds()/60)/60)
#print(FALL["Aufenthaltszeit in Stunden"] )
#FALL = FALL[FALL["Aufenthaltszeit in Stunden"] > 24]

fallnummern = FALL["KH-internes-Kennzeichen"].values
newpath = r'./P21_fuer_grouper/' 

for datei in GrouperDateien:
    table = pd.read_csv(datei,encoding="latin1",delimiter=";",na_filter=False,dtype=str)
    table = table[table["KH-internes-Kennzeichen"].isin(fallnummern)]
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    table.to_csv(newpath+datei,encoding="latin1",sep=";",index=False)