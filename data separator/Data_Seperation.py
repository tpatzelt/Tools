import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
import pandas as pd
import csv


analyte_dict = {
    "CREA" : ["SL_nz-krea","Crea","Creatinin","Krea","Kreatinin","KREA","CREA"],
    "GFR" : ["SL_nz-ckd-epi", "eGFR","eGFR CysC(CKD-EPI)", "GFR", "Glomeruläre Filtrationsrate"],
    "BLUTZUCKER" : ["SL_nz-glu", "Glukose","Glucose","BZ","YBZ","YBGABZ", "BZNÜ","BZ14", "GLUS"],
    "KALIUM" : ["Kalium","Kalium im Serum","K","K+","RM_K+","SL_nz-k","YK+"],
    "NATRIUM" : ["Natrium","Na","Na+","YNA+","NA"],
    "HÄMOGLOBIN" : ["Hämoglobin","HB","SL_nz-hb","YTHB"],
    "QUICK" : ["SL_nz-quick2", "QUICK"],
    "ALBUMIN" : ["SL_nz-alb","ALBUM"],
    "FOLSÄURE" : ["SL_nz-fol2"],
    "EIWEIß" : ["SL_nz-tp","TP", "Eiweiß", "Eiweiss"],
    "LEUKOZYTEN" : ["SL_nz-leuko","LEUK", "Leukozyten"],
    "PROBNP" : ["SL_nz-probnp"],
    "FERRITIN" : ["SL_nz-fer","FERRI"],
    "HBA1C" : ["SL_nz-hba1c","SL_nz-hba1c-cob","HBA1C"],
    "SO2" : ["SL_nz-so2-k","SL_nz-so2-a","YSO2","SOA2","SO2"],
    "PCO2" : ["SL_nz-pco2-k","YPCO2","YPCO2T", "PCO2V","PCO2A","PCO2K"],
    "PO2" : ["SL_nz-po2-k","YPO2","YPO2T","PO2"],
    "TROPONIN" : ["cTnT", "cTnI", "Trop", "Trop_T", "TROPONIN"]
    }


class SeperateGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=20, weight='bold')
        self.title('Seperate Files')

        self.analyt = 'CREA'
        self.results = ''
        self.length = 0

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


         #create Page where the locations for the data are set
        self.frame = FolderPage(parent=container,controller = self)
        self.frame.grid(row=0, column=0, sticky="nsew")


        self.frame2 = OutputPage(parent=container, controller=self)
        self.frame2.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()

    #different filedialogs to select path
    def askopeninputdatei(self):
        try:
            self.inputdatei = filedialog.askopenfile(parent=self,mode='rb',title='Choose a file').name
            self.frame.input_button.config(text=self.inputdatei[self.inputdatei.rfind('/')+1:])
        except:
            pass

    def askopenoutputfolder(self):
        try:
            self.outputordner= filedialog.askdirectory(parent=self,title="Choose a folder")
            self.frame.output_button.config(text=self.outputordner[self.outputordner.rfind('/')+1:])
        except:
            pass

    def closeall(self):
        self.destroy()

    def getInput(self,event):
        if self.inputdatei != None:
            self.input = pd.read_csv(self.inputdatei, encoding="latin1", sep=";", na_filter=False,
                dtype={'FALLNR':int, 'UNTERSUCHUNGSID':str, 'UNTERSUCHUNGSWERT':str,
                'UNTERSUCHUNGSEINHEIT':str, 'DATUM':str, 'KLARTEXT':str, 'NORMALWERT':str}, low_memory=False)
        self.createOutput()

    def createOutput(self):
        self.output = self.input[self.input['KLARTEXT'].apply(lambda x: x in analyte_dict[self.analyt])]
        self.results=len(self.output)
        self.length = len(self.input)
        print(self.results, self.length)
        self.output.to_csv(self.outputordner+'/Labor_{}.csv'.format(self.analyt),encoding="latin1",sep=";",index=False,quoting=csv.QUOTE_ALL)
        print('saved file')
        self.show_result()

    def show_result(self):
        self.frame2.label.config(text = 'Es bleiben {} von {} Einträgen übrig'.format(self.results, self.length))
        self.frame2.tkraise()


class FolderPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        #set elements on FolderPage
        tk.Label(self,text="Inputdatei(.csv/.docx)").grid(row=0,sticky=tk.W, padx=10,pady=10)
        self.input_button = tk.Button(self, text="Auswählen...",command= self.controller.askopeninputdatei)
        self.input_button.grid(row=0,column=2,sticky=tk.E, padx=1,pady=10)

        tk.Label(self,text="Output-Ordner").grid(row=1,sticky=tk.W, padx=10,pady=10)
        self.output_button = tk.Button(self, text="Auswählen...",command=self.controller.askopenoutputfolder)
        self.output_button.grid(row=1,column=2,sticky=tk.E, padx=1,pady=10)

        choice = tk.StringVar(self)
        # Dictionary with options
        choices = set(analyte_dict.keys())
        choice.set('CREA') # set the default option

        self.popupMenu = tk.OptionMenu(self, choice, *choices)
        tk.Label(self, text="Wähle Analyt").grid(row = 2, sticky=tk.W, padx=10, pady=10)
        self.popupMenu.grid(row = 2, column =2)

        # on change dropdown value
        def change_dropdown(*args):
            self.controller.analyt = choice.get()

        # link function to change dropdown
        choice.trace('w', change_dropdown)

        self.weiter_button = tk.Button(self, text="Datei erstellen!",command=self.destroy)
        self.weiter_button.grid(row=6,column=3,padx=10, pady=10, sticky=tk.S)
        self.weiter_button.bind("<1>",self.controller.getInput)


class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.label = tk.Label(self, text='Hallo')
        self.label.grid(row=0,sticky=tk.W, padx=10,pady=10)
        self.exit_button = tk.Button(self, text="Exit!",command=controller.closeall)
        self.exit_button.grid(row=6,column=3,padx=10,pady=10,sticky=tk.S)

class ErrorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.label = tk.Label(self, text='Hallo')
        self.label.grid(row=0,sticky=tk.W, padx=10,pady=10)
        self.exit_button = tk.Button(self, text="Exit!",command=controller.closeall)
        self.exit_button.grid(row=6,column=3,padx=10,pady=10,sticky=tk.S)

if __name__ == '__main__':

    window = SeperateGUI()
    window.mainloop()
