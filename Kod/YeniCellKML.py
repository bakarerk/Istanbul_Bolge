from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import simplekml
import ftplib
import pandas as pd

def getEndpoint(lat1, lon1, bearing, d):
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, d * 1852)
    return d['lat2'], d['lon2']

def descript(cell_name,site,antenna,azimuth,height,lactac,bcch,bsc):
    return '''
<style>
#customers {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #ddd;}

#customers th {
  padding-top: 8px;
  padding-bottom: 8px;
  text-align: left;
  background-color: #e64543;
  color: white;
}
</style>

<table id="customers">
   <tr>
    <th>Cell Name</th>
    <td>''' + str(cell_name) + '''</td>
  </tr>
  <tr>
    <th>Site</th>
     <td>''' + str(site) + '''</td>
  </tr>
  <tr>
    <th>Antenna</th>
     <td>''' + str(antenna) + '''</td>
  </tr>
  <tr>
    <th>Azimuth</th>
     <td>''' + str(azimuth) + '''</td>
  </tr>
  <tr>
    <th>Height</th>
     <td>''' + str(height) + '''</td>
  </tr>
  <tr>
    <th>LAC-TAC</th>
     <td>''' + str(lactac) + '''</td>
  </tr>
  <tr>
    <th>BCCH-PSC-PCI</th>
     <td>''' + str(bcch) + '''</td>
  </tr>
   <tr>
    <th>BSC-RNC</th>
     <td>''' + str(bsc) + '''</td>
  </tr>

</table>

'''

'''
path  = '/LibraryFiles/'
filename_1 = 'GSM_Engineering_CellDB.xls'
filename_2 = 'UMTS_Engineering_CellDB.xls'
filename_3 = 'LTE_Engineering_CellDB.xls'
ftp = ftplib.FTP("gmp2kaydemir")
ftp.login("opti", "optik")
ftp.cwd(path)
ftp.retrbinary("RETR " + filename_1 ,open(filename_1, 'wb').write)
ftp.retrbinary("RETR " + filename_2 ,open(filename_2, 'wb').write)
ftp.retrbinary("RETR " + filename_3 ,open(filename_3, 'wb').write)
ftp.quit()
'''

LTE = pd.read_csv("LTE_Engineering_CellDB.xls",sep="\t",low_memory=False,index_col="CELLNAME")
UMTS = pd.read_csv("UMTS_Engineering_CellDB.xls",sep="\t",low_memory=False,index_col="CELLNAME")
GSM = pd.read_csv("GSM_Engineering_CellDB.xls",sep="\t",low_memory=False,index_col="CELLNAME")

GSMDict = GSM.to_dict()
UMTSDict = UMTS.to_dict()
LTEDict = LTE.to_dict()

cellnameListGSM = list(GSM.index)
cellnameListUMTS = list(UMTS.index)
cellnameListLTE = list(LTE.index)

techSytle = {"GSM":{"beam":40,"inner":0,"outer":0.01,"color":"9864b736"}, \
             "UMTS":{"beam":40,"inner":0,"outer":0.01,"color":"851f03a4"}, \
             "6300":{"beam":40,"inner":0.011,"outer":0.02,"color":"85381e33"}, \
             "3725":{"beam":40,"inner":0.021,"outer":0.03,"color":"85ff00aa"}, \
             "1899":{"beam":40,"inner":0.031,"outer":0.04,"color":"85ff5500"}, \
             "301":{"beam":40,"inner":0.041,"outer":0.05,"color":"850095e5"}, \
             "3075":{"beam":40,"inner":0.051,"outer":0.06,"color":"85f69b45"}, \
             "37950":{"beam":40,"inner":0.061,"outer":0.07,"color":"85f69b45"}}

kml = simplekml.Kml()
site_folder = kml.newfolder(name='Site')
gsm_folder = kml.newfolder(name='GSM')
umts_folder = kml.newfolder(name='UMTS')
lte_folder = kml.newfolder(name='LTE')

####GSM KISMI
# CELLNAME	CITY	DISTRICT	REGION	SITE_NAME	Site_ID	LAC	CI	BCCHNO	NCC	BCC	BSC
# Lat_Site	Lon_Site	AZIMUTH	M_TILT	E_TILT	HEIGHT	TRX_NUM
for cellname in cellnameListGSM:
    city = GSMDict["CITY"][cellname]
    if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = GSMDict["Lat_Site"][cellname]
        lon = GSMDict["Lon_Site"][cellname]
        azimuth = GSMDict["AZIMUTH"][cellname]
        beam = techSytle["GSM"]["beam"]
        radius = techSytle["GSM"]["outer"]
        d1 = getEndpoint(lat,lon,azimuth,radius)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,radius)
        site = GSMDict["SITE_NAME"][cellname]
        antenna = ""
        height = GSMDict["HEIGHT"][cellname]
        lac = GSMDict["LAC"][cellname]
        bcch = GSMDict["BCCHNO"][cellname]
        bsc = GSMDict["BSC"][cellname]


        gsm_cell = gsm_folder.newpolygon(name=site)
        gsm_cell.outerboundaryis = [(lon,lat,10), (d1[1],d1[0],10),(d2[1],d2[0],10),(lon,lat,10)]
        gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
        gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
        gsm_cell.style.linestyle.width = 2.8
        gsm_cell.extrude = 1
        gsm_cell.altitudemode = simplekml.AltitudeMode.relativetoground
        gsm_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

####UMTS KISMI
#CELLNAME	SectorWithNodeBName	DC_Freqs	DC_Stat	DC_Cells	Sector	Site_ID	REGION	City	DISTRICT	NODEBNAME	NODEBID	CELLID
#LOCELL	BANDIND	UARFCNDOWNLINK	DL_Freq	UARFCNUPLINK	LAC	SAC	RAC	PSCRAMBCODE	TCELL	CIO	SPGID	ACTSTATUS	BLKSTATUS
# Lat_Site	Lon_Site	RNCNAME	AZIMUTH	M_TILT	E_TILT	HEIGHT	ANTENNA	CELLTYPE	RNCID	Strategy1	Comment
for cellname in cellnameListUMTS:
    city = UMTSDict["City"][cellname]
    if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = UMTSDict["Lat_Site"][cellname]
        lon = UMTSDict["Lon_Site"][cellname]
        azimuth = UMTSDict["AZIMUTH"][cellname]
        beam = techSytle["UMTS"]["beam"]
        radius = techSytle["UMTS"]["outer"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,radius)
        d2 = getEndpoint(lat,lon,azimuth,radius)
        site = UMTSDict["NODEBNAME"][cellname]
        antenna = UMTSDict["ANTENNA"][cellname]
        height = UMTSDict["HEIGHT"][cellname]
        lac = UMTSDict["LAC"][cellname]
        bcch = UMTSDict["PSCRAMBCODE"][cellname]
        bsc = UMTSDict["RNCNAME"][cellname]

        umts_cell = umts_folder.newpolygon(name=site)
        umts_cell.outerboundaryis = [(lon,lat,10), (d1[1],d1[0],10),(d2[1],d2[0],10),(lon,lat,10)]
        umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
        umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
        umts_cell.style.linestyle.width = 2.8
        umts_cell.extrude = 1
        umts_cell.altitudemode = simplekml.AltitudeMode.relativetoground
        umts_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

#LTE kosmı
#CELLNAME	EnodebName_CID	Sector	SiteID	CA_Stat	CA_Freqs	CITYCODE	MAIN_REGION	SUB_REGION
# City	DISTRICT	eNodebID	eNodebID_CellID	BandType	EnodebName	ENODEBFUNCTIONNAME	TAC	TAC_ATOLL
# LOCALCELLID	CELLID	TXRXMODE	FREQBAND	DLEARFCN	DL_Freq	SiteEARFCNs	DLBANDWIDTH	ULBANDWIDTH	PHYCELLID
# ROOTSEQUENCEIDX	PREAMBLEFMT	CELLRADIUS	CELLADMINSTATE	CELLACTIVESTATE	REFERENCESIGNALPWR	PAPCOFF	PB
# Lat_Site	Lon_Site	AZIMUTH	M_TILT	E_TILT	HEIGHT	ANTENNA	ANTENNA_BW	CellType	FreqType
# X1	X2	X3	X4	X5	X6	X7	X8	X9	X10	Vendor	NodeType	OSSIP

for cellname in cellnameListLTE:
    city = LTEDict["City"][cellname]
    if city == "EDIRNE" or city == "ISTANBUL" or city == "KIRKLARELI" or city == "TEKIRDAG":
        band = str(LTEDict["DLEARFCN"][cellname])
        lat = LTEDict["Lat_Site"][cellname]
        lon = LTEDict["Lon_Site"][cellname]
        azimuth = LTEDict["AZIMUTH"][cellname]
        beam = techSytle[band]["beam"]
        outer = techSytle[band]["outer"]
        inner = techSytle[band]["inner"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,outer)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,outer)
        d0 = getEndpoint(lat,lon,azimuth + beam/2,inner)
        d4 = getEndpoint(lat,lon,azimuth - beam/2,inner)
        site = LTEDict["EnodebName"][cellname]
        antenna = LTEDict["ANTENNA"][cellname]
        height = LTEDict["HEIGHT"][cellname]
        lac = LTEDict["TAC"][cellname]
        bcch = LTEDict["PHYCELLID"][cellname]
        bsc = ""

        pol = kml.newpolygon(name=site)
        pol.outerboundaryis = [(d0[1],d0[0]), (d1[1],d1[0]),(d2[1],d2[0]),(d4[1],d4[0])]
        pol.style.polystyle.color = techSytle[band]["color"]
        pol.style.linestyle.color = techSytle[band]["color"]
        #pol.style.linestyle.width = 4 * 0.7
        pol.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)
'''
kml.savekmz("Polygon Styling.kmz",False)

#print(newDictGSM["SITE_NAME"]["GM277020O6129802"])
#for i in newDictGSM.keys():
#    print(newDictGSM[i])
