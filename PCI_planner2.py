import pandas as pd
import geopy.distance

def distance_calc (row):
    start = (row['slat'], row['slon'])
    stop = (row['Lat_Site'], row['Lon_Site'])
    return geopy.distance.geodesic(start, stop).km

resultfile = open("result.txt",mode='w')
#resultfile2 = open("result2.txt",mode='w')
resultfile.write("MAIN_REGION" + "  " + "SUB_REGION" + "  " + "City" + "  " + "DISTRICT" + "  " + "eNodebID" + "  " + "eNodebID_CellID" + "  " + "EnodebName" + "  " + "LOCALCELLID" + "  " + "DLEARFCN" + "  " + "PHYCELLID" + "  " + "ROOTSEQUENCEIDX" + "  " + "Lat_Site" + "  " + "Lon_Site" + "  " + "AZIMUTH" + "  " + "CellType" + "  " + "new" + "  " + "SourceCellname" + "  " + "TargetCellname" + "  " + "SourceEnodebName" + "\n")
LTE = pd.read_csv("LTE_Engineering_CellDB.xls",sep="\t",usecols=["CELLNAME","MAIN_REGION","SUB_REGION","City","DISTRICT","eNodebID","eNodebID_CellID","EnodebName","LOCALCELLID","DLEARFCN","PHYCELLID","ROOTSEQUENCEIDX","Lat_Site","Lon_Site","AZIMUTH","CellType"],index_col="CELLNAME")
COLUMN_NAMES = ["MAIN_REGION","SUB_REGION","City","DISTRICT","eNodebID","eNodebID_CellID","EnodebName","LOCALCELLID","DLEARFCN","PHYCELLID","ROOTSEQUENCEIDX","Lat_Site","Lon_Site","AZIMUTH","CellType","Source","slat","slon","distance"]

LTE = LTE[LTE["CellType"] == "OUTDOOR"]
LTE = LTE[LTE["City"] == "ISTANBUL"]
LTE = LTE[LTE['Lat_Site'].notnull()]

LTE900 = LTE[LTE["DLEARFCN"] == 3725]
LTE800 = LTE[LTE["DLEARFCN"] == 6300]
LTE1800 = LTE[LTE["DLEARFCN"] == 1899]
LTE2100 = LTE[LTE["DLEARFCN"] == 301]
LTE2600 = LTE[LTE["DLEARFCN"] == 3075]

bandlar = [LTE900,LTE800,LTE1800,LTE2100,LTE2600]

for band in bandlar:
    cellnameList = sorted(list(band.index))
    for i in cellnameList:
        cellpci = band.at[i,"PHYCELLID"]
        print(cellpci,i)
        try:
            closeDF = band[band["PHYCELLID"] == cellpci]
            closeDF = closeDF.loc[(closeDF.index != i)]
            closeDF["Source"] = i
            closeDF["slat"] = band.at[i,"Lat_Site"]
            closeDF["slon"] = band.at[i, "Lon_Site"]
            closeDF['distance'] = closeDF.apply(lambda row: distance_calc(row), axis=1)
        except ValueError:
            closeDF['distance'] = 99999
            closeDF["Source"] = i
            closeDF["slat"] = 49.001
            closeDF["slon"] = 49.001
        enyakin = closeDF["distance"].min()
        enyakinDF = closeDF[closeDF["distance"] == enyakin]
        resultfile.write(enyakinDF.to_string(index=False,header=None) + "\n")
resultfile.close()
    #closeDF = closeDF.loc[(closeDF.index != source_cell)]
