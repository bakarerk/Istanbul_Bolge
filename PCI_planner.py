import pandas as pd
import geopy.distance
resultfile = open("result.txt",mode='w')
pd. set_option("display.max_columns", None)
LTE = pd.read_csv("LTE_Engineering_CellDB.xls",sep="\t",usecols=["CELLNAME","MAIN_REGION","SUB_REGION","City","DISTRICT","eNodebID","eNodebID_CellID","EnodebName","LOCALCELLID","DLEARFCN","PHYCELLID","ROOTSEQUENCEIDX","Lat_Site","Lon_Site","AZIMUTH","CellType"],index_col="CELLNAME")

LTE = LTE[LTE["CellType"] == "OUTDOOR"]
LTE = LTE[LTE["City"] == "ISTANBUL"]

LTE900 = LTE[LTE["DLEARFCN"] == 3725]
LTE900_dict = LTE900.to_dict()
cellnameListLTE900 = sorted(list(LTE900.index))

for source_cell in cellnameListLTE900:
    source_lat = LTE900_dict["Lat_Site"][source_cell]
    source_lon = LTE900_dict["Lon_Site"][source_cell]
    source_pci = LTE900_dict["PHYCELLID"][source_cell]
    source_rsi = LTE900_dict["ROOTSEQUENCEIDX"][source_cell]
    source_azimuth = LTE900_dict["AZIMUTH"][source_cell]
    source_earfcn = LTE900_dict["DLEARFCN"][source_cell]
    source_ccords = (source_lat,source_lon)

    #target cell, source ile aynı band ve pci sahip
    target_cell = LTE900.copy()
    target_cell = target_cell[target_cell["PHYCELLID"] == source_pci]
    target_cell = target_cell.loc[(target_cell.index != source_cell)]
    targetcellnameListLTE900 = sorted(list(target_cell.index))
    target_cell_dict = target_cell.to_dict()

    for target in targetcellnameListLTE900:
        target_lat = target_cell_dict["Lat_Site"][target]
        target_lon = target_cell_dict["Lon_Site"][target]

        target_ccords = (target_lat,target_lon)
        try:
            target_cell.at[target,"new"] = geopy.distance.vincenty(source_ccords, target_ccords).km
            target_cell.at[target, "SourceCellname"] = source_cell
            target_cell.at[target, "TargetCellname"] = target
        except ValueError:
            target_cell.at[target, "new"] = 99999

    enyakin = target_cell["new"].min()
    print(target_cell[target_cell["new"] == enyakin].to_string(index=False,header=None))
    resultfile.write(target_cell[target_cell["new"] == enyakin].to_string(index=False,header=None) + "\n")

resultfile.close()


