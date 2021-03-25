import pandas as pd
import numpy as np
from functools import reduce
import os

# import time
cwd = os.getcwd()


# t = time.process_time()

def siteid(site):
    if site[0] == "B":
        return str(site[4:9])
    elif site[0] == "N":
        return str(site[12:17])
    elif site[0] == "G" or site[0] == "S":
        return str(site[5:10])
    else:
        return site


def siteidTamamla(site):
    siteLen = len(str(site))
    if siteLen < 5:
        return "{}{}".format("0" * (5 - siteLen), site)
    else:
        return site


def cacount(ca):
    if ca == 0:
        return 0
    elif ca.count("-") == 5:
        return 5
    else:
        return ca.count("-") + 1


def sitedistance(x):
    if x > 2.5:
        return 1
    else:
        return 0.2


def indoor(x):
    if x == "INDOOR":
        return 1
    else:
        return 0.2


def fplan5g(x):
    if x == 1:
        return 1
    else:
        return 0.2


def fotherop(x):
    if x == "3 OPT":
        return 1
    elif x == "2 OPT":
        return 7 / 9
    else:
        return 4 / 9


def util(x):
    if x >= 100:
        return 1
    elif x < 100 and x >= 70:
        return 0.7
    elif x < 70 and x >= 50:
        return 0.5
    elif x < 50 and x >= 20:
        return 0.4
    elif x < 20 and x > 0:
        return 0.3
    else:
        return 0.2


dude = pd.read_excel("Dude.xlsx", sheet_name="Site", skiprows=2,
                     usecols=["REGION", "CITY", "LAYER", "COMMON ID", "# of IMEI", "# of FAKE", "GSM", "UMTS", "LTE"])
# dude = dude.loc[(dude['REGION'] == "Istanbul") & ((dude['LAYER'] == "LTE") | (dude['LAYER'] == "TOTAL") | (dude['LAYER'] == "UMTS"))]

dude_lte_fake = dude.loc[(dude["LAYER"] == "LTE")][["COMMON ID", "# of FAKE"]]
dude_lte_total = dude.loc[(dude["LAYER"] == "TOTAL")][["COMMON ID", "LTE"]]
dude_umts_fake = dude.loc[(dude["LAYER"] == "UMTS")][["COMMON ID", "# of FAKE"]]
dude_umts_total = dude.loc[(dude["LAYER"] == "TOTAL")][["COMMON ID", "UMTS"]]
dude_total = dude.loc[(dude["LAYER"] == "TOTAL")][["COMMON ID", "# of IMEI"]]

dudelist = [dude_lte_fake, dude_lte_total, dude_umts_fake, dude_umts_total, dude_total]
dude_final = reduce(lambda left, right: pd.merge(left, right, on='COMMON ID'), dudelist)
dude_final["SITEID"] = dude_final["COMMON ID"].apply(siteidTamamla)
dude_final.to_excel("dude_final.xlsx")

# elapsed_time = time.process_time() - t
# print("{}:{}".format(1,elapsed_time))

lteDB = pd.read_csv(cwd + '/LTE_Engineering_CellDB.xls', sep="\t", low_memory=False)
lteDB["SITEID"] = lteDB["EnodebName"].apply(siteid)
lteIndoor = lteDB.loc[lteDB["CellType"] == "INDOOR"]
lteIndoor = lteIndoor[["SITEID", "CellType"]]
lteIndoor.dropna()
lteIndoor = lteIndoor.drop_duplicates()
lteDB = lteDB[["SITEID", "SiteEARFCNs", "City", "DISTRICT"]]
lteDB.dropna(subset=["City", "DISTRICT"], inplace=True)
lteDB = lteDB.drop_duplicates()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(2,elapsed_time))

umtsDB = pd.read_csv(cwd + '/UMTS_Engineering_CellDB.xls', sep="\t", low_memory=False)
umtsDB["SITEID"] = umtsDB["NODEBNAME"].apply(siteid)
umtsDB = umtsDB[["SITEID", "City", "DISTRICT"]]
umtsDB.dropna(subset=["City", "DISTRICT"], inplace=True)
umtsDB = umtsDB.drop_duplicates()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(3,elapsed_time))

gsmDB = pd.read_csv(cwd + '\GSM_Engineering_CellDB.xls', sep="\t", low_memory=False)
gsmDB.dropna(subset=["SITE_NAME"], inplace=True)
gsmDB["SITEID"] = gsmDB["SITE_NAME"].apply(siteid)
gsmDB = gsmDB[["SITEID", "CITY", "DISTRICT"]]
gsmDB.dropna(subset=["CITY", "DISTRICT"], inplace=True)
gsmDB = gsmDB.drop_duplicates()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(4,elapsed_time))

traffic2G = pd.read_excel(cwd + '/2G.xlsx', sheet_name='Sheet')
traffic2G = traffic2G[['BTS_NAME', 'SHM_TCHTRAFFIC', 'HM_TOT_2G_DATA_TRAFF_KB']]
traffic2G["SITEID"] = traffic2G["BTS_NAME"].apply(siteid)
traffic2G.rename(
    columns={'BTS_NAME': '2G_SITE', 'SHM_TCHTRAFFIC': '2G_VOICE_TRAFFIC', 'HM_TOT_2G_DATA_TRAFF_KB': '2G_DATA_TRAFFIC'},
    inplace=True)
traffic2G = traffic2G.drop_duplicates()
traffic2G = traffic2G.groupby(['2G_SITE', 'SITEID'])[['2G_VOICE_TRAFFIC', '2G_DATA_TRAFFIC']].agg('sum').reset_index()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(5,elapsed_time))

traffic3G = pd.read_excel(cwd + '/3G.xlsx', sheet_name='Sheet')
traffic3G = traffic3G[['NODEB_NAME', 'SH_CS_TRAFFIC_TOTAL', 'TOT_3G_TRAF_MB']]
traffic3G["SITEID"] = traffic3G["NODEB_NAME"].apply(siteid)
traffic3G.rename(
    columns={'NODEB_NAME': '3G_SITE', 'SH_CS_TRAFFIC_TOTAL': '3G_VOICE_TRAFFIC', 'TOT_3G_TRAF_MB': '3G_DATA_TRAFFIC'},
    inplace=True)
traffic3G = traffic3G.drop_duplicates()
traffic3G = traffic3G.groupby(['3G_SITE', 'SITEID'])[['3G_VOICE_TRAFFIC', '3G_DATA_TRAFFIC']].agg('sum').reset_index()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(6,elapsed_time))

traffic4G = pd.read_excel(cwd + '/LTE.xlsx', sheet_name='Sheet')
traffic4G = traffic4G[['ENODEB_NAME', 'VOLTE_TRAFFIC', 'DATA_TRAFFIC_VOL_MB']]
traffic4G["SITEID"] = traffic4G["ENODEB_NAME"].apply(siteid)
traffic4G.rename(
    columns={'ENODEB_NAME': '4G_SITE', 'VOLTE_TRAFFIC': '4G_VOICE_TRAFFIC', 'DATA_TRAFFIC_VOL_MB': '4G_DATA_TRAFFIC'},
    inplace=True)
traffic4G = traffic4G.drop_duplicates()
traffic4G = traffic4G.groupby(['4G_SITE', 'SITEID'])[['4G_VOICE_TRAFFIC', '4G_DATA_TRAFFIC']].agg('sum').reset_index()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(7,elapsed_time))

util4g = pd.read_excel(cwd + '/Report 4G UtilPRB.xlsx', usecols=['ENODEB_NAME', 'KPI160_3'], sheet_name='Sheet')
# util4g = util4g[['ENODEB_NAME', 'KPI160_3']]
util4g["SITEID"] = util4g["ENODEB_NAME"].apply(siteid)
util4g = util4g.groupby(['SITEID'])[['KPI160_3']].agg('max').reset_index()
# print(util4g)

# elapsed_time = time.process_time() - t
# print("{}:{}".format(8,elapsed_time))

roamer = pd.read_excel(cwd + '/SiteScore_Roamer.xlsx')
roamer["SITEID"] = roamer["Sitename"].apply(siteid)
roamer = roamer[["SITEID", "2G Voice.Counters.Imsi Cnt", "3G Voice.Counters.Imsi Cnt"]]
roamer.fillna(0, inplace=True)
roamer["TOTAL_ROAMER"] = roamer["2G Voice.Counters.Imsi Cnt"] + roamer["3G Voice.Counters.Imsi Cnt"]
roamer = roamer.groupby(['SITEID'])[['TOTAL_ROAMER']].agg('sum').reset_index()

# elapsed_time = time.process_time() - t
# print("{}:{}".format(9,elapsed_time))

hotspot = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="HOTSPOT")
hotspot = hotspot[["SITEID", "HOTSPOT_FLAG"]]
reveneu = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="REVENEU")
reveneu = reveneu[["SITEID", "REVENEU"]]
plan5g = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="5G")
plan5g = plan5g[["SITEID", "5G_PLAN"]]
otherop = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="OTHER_OP")
otherop = otherop[["SITEID", "OTHER_OP"]]
p3 = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="P3")
p3 = p3[["SITEID", "P3_Occurence"]]
distance = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="DISTANCE")
distance = distance[["SITEID", "AVG_DISTANCE"]]
puanlama = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="PUANLAMA")
puanlama.set_index("BASLIK", inplace=True)
hotspotcategory = pd.read_excel(cwd + "/SITESCORE_MAIN.xlsx", sheet_name="HOTSPOT_KATEGORI")
hotspotcategory.set_index("HOTSPOT_FLAG", inplace=True)

# elapsed_time = time.process_time() - t
# print("{}:{}".format(10,elapsed_time))

uniq_site = (traffic2G["SITEID"].append(traffic3G["SITEID"]).append(traffic4G["SITEID"])).drop_duplicates()

sitescorelist = [uniq_site, traffic2G, traffic3G, traffic4G, roamer, lteDB, umtsDB, gsmDB, hotspot, lteIndoor, reveneu,
                 plan5g, otherop, p3, dude_final, distance, util4g]
site_score_final = reduce(lambda left, right: pd.merge(left, right, on='SITEID', how='left'), sitescorelist)
site_score_final.fillna(0, inplace=True)

sitescorelist2 = [site_score_final, hotspotcategory]
site_score_final = reduce(lambda left, right: pd.merge(left, right, on='HOTSPOT_FLAG', how='left'), sitescorelist2)
site_score_final.fillna(0, inplace=True)

# elapsed_time = time.process_time() - t
# print("{}:{}".format(11,elapsed_time))

# data işleme kısmı
site_score_final["TOTAL_VOICE"] = site_score_final["2G_VOICE_TRAFFIC"] + site_score_final["3G_VOICE_TRAFFIC"] + \
                                  site_score_final["4G_VOICE_TRAFFIC"]
site_score_final["TOTAL_DATA"] = (site_score_final["2G_DATA_TRAFFIC"] / 1024 + site_score_final["3G_DATA_TRAFFIC"] +
                                  site_score_final[
                                      "4G_DATA_TRAFFIC"]) / 1024

site_score_final["LTE_DUDE"] = site_score_final["# of FAKE_x"] + site_score_final["LTE"]
site_score_final["ALL_DUDE"] = site_score_final["# of IMEI"]

p40_dude = site_score_final.quantile(0.4)  # ,"TOTAL_DATA","LTE_DUDE","ALL_DUDE"]
p50_dude = site_score_final.quantile(0.5)  # ,"TOTAL_DATA","LTE_DUDE","ALL_DUDE"]
p60_dude = site_score_final.quantile(0.6)  # ,"TOTAL_DATA","LTE_DUDE","ALL_DUDE"]
p70_dude = site_score_final.quantile(0.7)  # ,"TOTAL_DATA","LTE_DUDE","ALL_DUDE"]
p80_dude = site_score_final.quantile(0.8)  # ,"TOTAL_DATA","LTE_DUDE","ALL_DUDE"]
p90_dude = site_score_final.quantile(0.9)  # ,"TOTAL_DATA","LTE_DUDE","ALL_DUDE"]
p100_dude = site_score_final.quantile(1)

# elapsed_time = time.process_time() - t
# print("{}:{}".format(12,elapsed_time))

for column in ["TOTAL_VOICE", "TOTAL_DATA", "LTE_DUDE", "ALL_DUDE", "REVENEU", "TOTAL_ROAMER"]:
    criteria = [site_score_final[column].between(0, p40_dude[column]),
                site_score_final[column].between(p40_dude[column], p50_dude[column]),
                site_score_final[column].between(p50_dude[column], p60_dude[column]),
                site_score_final[column].between(p60_dude[column], p70_dude[column]),
                site_score_final[column].between(p70_dude[column], p80_dude[column]),
                site_score_final[column].between(p80_dude[column], p90_dude[column]),
                site_score_final[column].between(p90_dude[column], p100_dude[column])]
    values = [3, 4, 5, 6, 7, 8, 9]
    newcolumn = "{}{}".format(column, "_P")
    site_score_final[newcolumn] = np.select(criteria, values, 0)
site_score_final.fillna(0, inplace=True)

# elapsed_time = time.process_time() - t
# print("{}:{}".format(13,elapsed_time))

site_score_final["FINAL_CS"] = puanlama.at["FINAL_CS", "PUAN"] * site_score_final["TOTAL_VOICE_P"]
site_score_final["FINAL_PS"] = puanlama.at["FINAL_PS", "PUAN"] * site_score_final["TOTAL_DATA_P"]
site_score_final["FINAL_UTIL"] = site_score_final["KPI160_3"].apply(util)
site_score_final["FINAL_HOTSPOT"] = puanlama.at["FINAL_HOTSPOT", "PUAN"] * site_score_final[
    ["HOTSPOT_PUAN", "FINAL_UTIL"]].max(axis=1)
site_score_final["FINAL_CA"] = site_score_final["SiteEARFCNs"].apply(cacount)
site_score_final["FINAL_TERMINAL"] = puanlama.at["FINAL_TERMINAL", "PUAN"] * site_score_final["LTE_DUDE_P"]
site_score_final["FINAL_SITEDISTANCE"] = puanlama.at["FINAL_SITEDISTANCE", "PUAN"] * site_score_final[
    "AVG_DISTANCE"].apply(sitedistance)
site_score_final["FINAL_ROAMER"] = puanlama.at["FINAL_ROAMER", "PUAN"] * site_score_final["TOTAL_ROAMER_P"]
site_score_final["FINAL_INDOOR"] = puanlama.at["FINAL_INDOOR", "PUAN"] * site_score_final["CellType"].apply(indoor)
site_score_final["FINAL_REVENEU"] = puanlama.at["FINAL_REVENEU", "PUAN"] * site_score_final["REVENEU_P"]
site_score_final["FINAL_5G"] = puanlama.at["FINAL_5G", "PUAN"] * site_score_final["5G_PLAN"].apply(fplan5g)
site_score_final["FINAL_P3"] = puanlama.at["FINAL_P3", "PUAN"] * site_score_final["P3_Occurence"]
site_score_final["FINAL_OTHEROPERATOR"] = puanlama.at["FINAL_OTHEROPERATOR", "PUAN"] * site_score_final[
    "OTHER_OP"].apply(fotherop)
site_score_final["SITE_SCORE"] = site_score_final["FINAL_CS"] + site_score_final["FINAL_PS"] + site_score_final[
    "FINAL_HOTSPOT"] + site_score_final["FINAL_CA"] + site_score_final["FINAL_TERMINAL"] + site_score_final[
                                     "FINAL_SITEDISTANCE"] + site_score_final["FINAL_ROAMER"] + site_score_final[
                                     "FINAL_INDOOR"] + site_score_final["FINAL_REVENEU"] + site_score_final[
                                     "FINAL_5G"] + site_score_final["FINAL_P3"] + site_score_final[
                                     "FINAL_OTHEROPERATOR"]

# elapsed_time = time.process_time() - t
# print("{}:{}".format(14,elapsed_time))

site_score_ozet = site_score_final[
    ["SITEID", "City_x", "DISTRICT_x", "City_y", "DISTRICT_y", "CITY", "DISTRICT", "2G_SITE", "3G_SITE", "4G_SITE",
     "TOTAL_VOICE", "TOTAL_DATA", "HOTSPOT_FLAG", "SiteEARFCNs", "LTE_DUDE", "AVG_DISTANCE", "TOTAL_ROAMER", "CellType",
     "REVENEU", "5G_PLAN", "P3_Occurence", "OTHER_OP", "FINAL_CS", "FINAL_PS", "FINAL_HOTSPOT", "FINAL_CA",
     "FINAL_TERMINAL", "FINAL_SITEDISTANCE", "FINAL_ROAMER", "FINAL_INDOOR", "FINAL_REVENEU", "FINAL_5G", "FINAL_P3",
     "FINAL_OTHEROPERATOR", "SITE_SCORE"]]

site_score_final.to_excel("site_score_final.xlsx")
site_score_ozet.to_excel("site_score_ozet.xlsx")