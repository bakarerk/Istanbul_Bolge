import pandas as pd

LTE = pd.read_csv("LTE_Engineering_CellDB.xls",sep="\t")
UMTS = pd.read_csv("UMTS_Engineering_CellDB.xls",sep="\t")
GSM = pd.read_csv("GSM_Engineering_CellDB.xls",sep="\t")

LTE_rfopt = LTE[["EnodebName","SiteID","LOCALCELLID","TAC","CELLNAME","PHYCELLID","ROOTSEQUENCEIDX","DLEARFCN","REFERENCESIGNALPWR","AZIMUTH","ANTENNA","HEIGHT","M_TILT","E_TILT","Lat_Site","Lon_Site"]]

LTE_rfopt.rename(columns={"EnodebName":"Site_Name","SiteID":"Site_ID","LOCALCELLID":"Cell_ID","TAC":"LAC","CELLNAME":"Cell_Name","PHYCELLID":"PCI_PSC_BCCH", \
                          "ROOTSEQUENCEIDX":"BSIC_Octet","DLEARFCN":"Freq","REFERENCESIGNALPWR":"Pcpich_Pwr","AZIMUTH":"Azimuth","ANTENNA":"Antenna_Type", \
                          "HEIGHT":"Antenna_Height","M_TILT":"Mtilt","E_TILT":"Etilt","Lat_Site":"Latitude","Lon_Site":"Longitude"},inplace="True")

LTE_rfopt["Site_ID"] = LTE_rfopt["Site_ID"].str[1:]
LTE_rfopt["Mode"] = "4G"
LTE_rfopt["RNC_BSC"] = " "
LTE_rfopt["RNC_ID"] = " "
LTE_rfopt["Max_Tx"] = " "
LTE_rfopt["Antenna_HBw"] = " "
LTE_rfopt["Antenna_VBw"] = " "
LTE_rfopt["NCC"] = " "
LTE_rfopt["BCC"] = " "
#LAC CI indoor outdoor bilgisi olarak kullanıyoruz şimdilik
LTE_rfopt["LACCI"] = LTE_rfopt["Cell_Name"].str[8]
LTE_rfopt["Target_CI"] = " "

LTE_rfopt = LTE_rfopt[["Site_Name","Site_ID","Cell_ID","LAC","Cell_Name","PCI_PSC_BCCH","BSIC_Octet","RNC_BSC","RNC_ID","Freq","Max_Tx","Pcpich_Pwr","Azimuth","Antenna_Type","Antenna_Height","Mtilt","Etilt","Antenna_HBw","Antenna_VBw","NCC","BCC","Latitude","Longitude","Mode","LACCI","Target_CI"]]

LTE_rfopt.to_csv("test1.txt",sep="\t")

LTE_indoor = LTE_rfopt[LTE_rfopt.LACCI == "I"]
LTE_outdoor = LTE_rfopt[LTE_rfopt.LACCI == "O"]

L800_indoor = LTE_indoor[LTE_indoor.Freq == 6300]
L900_indoor = LTE_indoor[LTE_indoor.Freq == 3725]
L1800_indoor = LTE_indoor[LTE_indoor.Freq == 1899]
L2100_indoor = LTE_indoor[LTE_indoor.Freq == 301]
L2600_indoor = LTE_indoor[LTE_indoor.Freq == 3075]

L800_outdoor = LTE_outdoor[LTE_outdoor.Freq == 6300]
L900_outdoor = LTE_outdoor[LTE_outdoor.Freq == 3725]
L1800_outdoor = LTE_outdoor[LTE_outdoor.Freq == 1899]
L2100_outdoor = LTE_outdoor[LTE_outdoor.Freq == 301]
L2600_outdoor = LTE_outdoor[LTE_outdoor.Freq == 3075]
Massive_outdoor = LTE_outdoor[LTE_outdoor.Freq == 37950]

L800_indoor.to_csv("LTE_L800_indoor.txt",sep="\t",index=False)
L900_indoor.to_csv("LTE_L900_indoor.txt",sep="\t",index=False)
L1800_indoor.to_csv("LTE_L1800_indoor.txt",sep="\t",index=False)
L2100_indoor.to_csv("LTE_L2100_indoor.txt",sep="\t",index=False)
L2600_indoor.to_csv("LTE_L2600_indoor.txt",sep="\t",index=False)
L800_outdoor.to_csv("LTE_L800_outdoor.txt",sep="\t",index=False)
L900_outdoor.to_csv("LTE_L900_outdoor.txt",sep="\t",index=False)
L1800_outdoor.to_csv("LTE_L1800_outdoor.txt",sep="\t",index=False)
L2100_outdoor.to_csv("LTE_L2100_outdoor.txt",sep="\t",index=False)
L2600_outdoor.to_csv("LTE_L2600_outdoor.txt",sep="\t",index=False)
Massive_outdoor.to_csv("LTE_massive.txt",sep="\t",index=False)

#'"EnodebName","SiteID","LOCALCELLID","TAC","CELLNAME","PHYCELLID","ROOTSEQUENCEIDX","","","DLEARFCN","","REFERENCESIGNALPWR","AZIMUTH","ANTENNA","HEIGHT","M_TILT","E_TILT","","","","","Lat_Site","Lon_Site","4G","""

