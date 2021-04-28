from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import simplekml
import ftplib
import pandas as pd
from polycircles import polycircles

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
    <td>''' + str(site) + '''</td>
  </tr>
  <tr>
    <th>Site</th>
     <td>''' + str(cell_name) + '''</td>
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


cellnameListGSM = sorted(list(GSM.index))
cellnameListUMTS = sorted(list(UMTS.index))
cellnameListLTE = sorted(list(LTE.index))

techSytle = {"GSM":{"beam":40,"inner":0,"inner_ind":4,"outer":0.02,"outer_ind":10,"color":"9864b736"}, \
             "UMTS":{"beam":40,"inner":0,"inner_ind":10,"outer":0.02,"outer_ind":16,"color":"851f03a4"}, \
             "6300":{"beam":40,"inner":0.02,"inner_ind":16,"outer":0.025,"outer_ind":19,"color":"85381e33"}, \
             "3725":{"beam":40,"inner":0.025,"inner_ind":19,"outer":0.03,"outer_ind":22,"color":"85ff00aa"}, \
             "1899":{"beam":40,"inner":0.03,"inner_ind":22,"outer":0.035,"outer_ind":25,"color":"85ff5500"}, \
             "301":{"beam":40,"inner":0.035,"inner_ind":25,"outer":0.04,"outer_ind":28,"color":"850095e5"}, \
             "3075":{"beam":40,"inner":0.04,"inner_ind":28,"outer":0.045,"outer_ind":31,"color":"85f69b45"}, \
             "37950":{"beam":40,"inner":0.045,"inner_ind":31,"outer":0.05,"outer_ind":34,"color":"85f69b45"}}
cellwidth = 2
h = 10

kml_trakya = simplekml.Kml()
site_folder = kml_trakya.newfolder(name='Site')
gsm_folder = kml_trakya.newfolder(name='GSM')
umts_folder = kml_trakya.newfolder(name='UMTS')
lte_folder = kml_trakya.newfolder(name='LTE')
site_folder.visibility = 0

avrupa_list = ['BEYLIKDUZU', 'BAKIRKOY', 'BESIKTAS', 'FATIH', 'EYUPSULTAN', 'GAZIOSMANPASA', 'BEYOGLU',
                    'KAGITHANE', 'SARIYER', 'ZEYTINBURNU', 'SISLI', 'KUCUKCEKMECE', 'CATALCA',
                    'AVCILAR', 'SILIVRI', 'BAHCELIEVLER', 'ESENYURT', 'ARNAVUTKOY', 'BUYUKCEKMECE',
                    'BAGCILAR', 'BASAKSEHIR', 'ESENLER', 'BAYRAMPASA', 'GUNGOREN', 'SULTANGAZI']
asya_list = ['KADIKOY', 'USKUDAR', 'TUZLA', 'SANCAKTEPE', 'BEYKOZ', 'CEKMEKOY', 'PENDIK', 'KARTAL',
                  'MALTEPE', 'UMRANIYE', 'SILE', 'ATASEHIR', 'ADALAR', 'SULTANBEYLI']
trakya_list = ['TEKIRDAG', 'EDIRNE', 'KIRKLARELI']

dic_site = {}
dic_gsm = {}
dic_umts = {}
dic_lte = {}
for i in trakya_list:
    dic_site[i] = site_folder.newfolder()
    dic_site[i].name = i
    dic_gsm[i] = gsm_folder.newfolder()
    dic_gsm[i].name = i
    dic_umts[i] = umts_folder.newfolder()
    dic_umts[i].name = i
    dic_lte[i] =  lte_folder.newfolder()
    dic_lte[i].name  = i


SITEDICT = {}
for cell in cellnameListGSM:
    lat = GSMDict["Lat_Site"][cell]
    lon = GSMDict["Lon_Site"][cell]
    city = GSMDict["CITY"][cell]
    district = GSMDict["DISTRICT"][cell]
    sitename = GSMDict["SITE_NAME"][cell]
    siteid = cell[1:6]
    SITEDICT[siteid] = [sitename,lat,lon,city,district]
for cell in cellnameListUMTS:
    lat = UMTSDict["Lat_Site"][cell]
    lon = UMTSDict["Lon_Site"][cell]
    city = UMTSDict["City"][cell]
    district = UMTSDict["DISTRICT"][cell]
    sitename = UMTSDict["NODEBNAME"][cell]
    siteid = cell[1:6]
    SITEDICT[siteid] = [sitename,lat,lon,city,district]
for cell in cellnameListLTE:
    lat = LTEDict["Lat_Site"][cell]
    lon = LTEDict["Lon_Site"][cell]
    city = LTEDict["City"][cell]
    district = LTEDict["DISTRICT"][cell]
    sitename = LTEDict["EnodebName"][cell]
    siteid = cell[1:6]
    SITEDICT[siteid] = [sitename,lat,lon,city,district]

# SITE KISMI
for siteid in SITEDICT.keys():
    city = SITEDICT[siteid][3]
    if city in trakya_list:
        style = simplekml.Style()
        lat = SITEDICT[siteid][1]
        lon = SITEDICT[siteid][2]
        site_name = SITEDICT[siteid][0]
        pnt = dic_site[city].newpoint(name=site_name, coords=[(lon, lat)])
        pnt.style.labelstyle.scale = 0.7
        pnt.iconstyle.scale = 0.5
        pnt.iconstyle.color = 'ff0000ff'
        pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
####GSM KISMI
# CELLNAME	CITY	DISTRICT	REGION	SITE_NAME	Site_ID	LAC	CI	BCCHNO	NCC	BCC	BSC
# Lat_Site	Lon_Site	AZIMUTH	M_TILT	E_TILT	HEIGHT	TRX_NUM
for cellname in cellnameListGSM:
    city = GSMDict["CITY"][cellname]
    if city in trakya_list:
    #if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
    #
        lat = GSMDict["Lat_Site"][cellname]
        lon = GSMDict["Lon_Site"][cellname]
        azimuth = GSMDict["AZIMUTH"][cellname]
        beam = techSytle["GSM"]["beam"]
        outer_ind = techSytle["GSM"]["outer_ind"]
        inner_ind = techSytle["GSM"]["inner_ind"]
        radius = techSytle["GSM"]["outer"]
        d1 = getEndpoint(lat,lon,azimuth,radius)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,radius)
        site = GSMDict["SITE_NAME"][cellname]
        antenna = ""
        height = GSMDict["HEIGHT"][cellname]
        lac = GSMDict["LAC"][cellname]
        bcch = GSMDict["BCCHNO"][cellname]
        bsc = GSMDict["BSC"][cellname]

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat,longitude=lon, radius=inner_ind, number_of_vertices=36)
            gsm_cell = dic_gsm[city].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(), outerboundaryis=indoor_outer.to_kml())
            gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
            gsm_cell.extrude = 1
            gsm_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            gsm_cell = dic_gsm[city].newpolygon(name=cellname)
            gsm_cell.outerboundaryis = [(lon,lat,h), (d1[1],d1[0],h),(d2[1],d2[0],h),(lon,lat,h)]
            gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.width = cellwidth
            gsm_cell.extrude = 1
            gsm_cell.style.polystyle.fill = 1
            gsm_cell.outline = 1
            gsm_cell.altitudemode = simplekml.AltitudeMode.relativetoground
            gsm_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

####UMTS KISMI
#CELLNAME	SectorWithNodeBName	DC_Freqs	DC_Stat	DC_Cells	Sector	Site_ID	REGION	City	DISTRICT	NODEBNAME	NODEBID	CELLID
#LOCELL	BANDIND	UARFCNDOWNLINK	DL_Freq	UARFCNUPLINK	LAC	SAC	RAC	PSCRAMBCODE	TCELL	CIO	SPGID	ACTSTATUS	BLKSTATUS
# Lat_Site	Lon_Site	RNCNAME	AZIMUTH	M_TILT	E_TILT	HEIGHT	ANTENNA	CELLTYPE	RNCID	Strategy1	Comment
for cellname in cellnameListUMTS:
    city = UMTSDict["City"][cellname]
    if city in trakya_list:
    #if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = UMTSDict["Lat_Site"][cellname]
        lon = UMTSDict["Lon_Site"][cellname]
        azimuth = UMTSDict["AZIMUTH"][cellname]
        beam = techSytle["UMTS"]["beam"]
        radius = techSytle["UMTS"]["outer"]
        outer_ind = techSytle["UMTS"]["outer_ind"]
        inner_ind = techSytle["UMTS"]["inner_ind"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,radius)
        d2 = getEndpoint(lat,lon,azimuth,radius)
        site = UMTSDict["NODEBNAME"][cellname]
        antenna = UMTSDict["ANTENNA"][cellname]
        height = UMTSDict["HEIGHT"][cellname]
        lac = UMTSDict["LAC"][cellname]
        bcch = UMTSDict["PSCRAMBCODE"][cellname]
        bsc = UMTSDict["RNCNAME"][cellname]

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            umts_cell = dic_umts[city].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(), outerboundaryis=indoor_outer.to_kml())
            umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
            umts_cell.extrude = 1
            umts_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            umts_cell = dic_umts[city].newpolygon(name=cellname)
            umts_cell.outerboundaryis = [(lon,lat,h), (d1[1],d1[0],h),(d2[1],d2[0],h),(lon,lat,h)]
            umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.width = cellwidth
            umts_cell.extrude = 1
            umts_cell.style.polystyle.fill = 1
            umts_cell.outline = 1
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
    if city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
    #if city == "EDIRNE" or city == "ISTANBUL" or city == "KIRKLARELI" or city == "TEKIRDAG":
        band = str(LTEDict["DLEARFCN"][cellname])
        lat = LTEDict["Lat_Site"][cellname]
        lon = LTEDict["Lon_Site"][cellname]
        azimuth = LTEDict["AZIMUTH"][cellname]
        beam = techSytle[band]["beam"]
        outer = techSytle[band]["outer"]
        outer_ind = techSytle[band]["outer_ind"]
        inner = techSytle[band]["inner"]
        inner_ind = techSytle[band]["inner_ind"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,outer)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,outer)
        d0 = getEndpoint(lat,lon,azimuth + beam/2,inner)
        d4 = getEndpoint(lat,lon,azimuth - beam/2,inner)
        midin = getEndpoint(lat,lon,azimuth,inner+0.002)
        midout = getEndpoint(lat,lon,azimuth,outer+0.002)
        site = LTEDict["EnodebName"][cellname]
        antenna = LTEDict["ANTENNA"][cellname]
        height = LTEDict["HEIGHT"][cellname]
        lac = LTEDict["TAC"][cellname]
        bcch = LTEDict["PHYCELLID"][cellname]
        bsc = ""
        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            lte_cell = dic_lte[city].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(), outerboundaryis=indoor_outer.to_kml())
            lte_cell.style.polystyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.color = techSytle[band]["color"]
            lte_cell.extrude = 1
            lte_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            lte_cell = dic_lte[city].newpolygon(name=cellname)
            #lte_cell.outerboundaryis = [(d2[1],d2[0],h),(d1[1],d1[0],h),(d0[1],d0[0],h),(d4[1],d4[0],h)]
            lte_cell.outerboundaryis = [(d0[1],d0[0],h), (d1[1],d1[0],h),(midout[1],midout[0],h),(d2[1],d2[0],h),(d4[1],d4[0],h),(midin[1],midin[0],h),(d0[1],d0[0],h)]
            lte_cell.style.polystyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.width = cellwidth
            lte_cell.extrude = 1
            lte_cell.style.polystyle.fill = 1
            lte_cell.outline = 1
            lte_cell.altitudemode = simplekml.AltitudeMode.relativetoground
            lte_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

kml_trakya.savekmz("TRAKYA.kmz",False)

#print(newDictGSM["SITE_NAME"]["GM277020O6129802"])
#for i in newDictGSM.keys():
#    print(newDictGSM[i])

'''
AVRUPA
'''
kml_avrupa = simplekml.Kml()
site_folder_avrupa = kml_avrupa.newfolder(name='Site')
gsm_folder_avrupa = kml_avrupa.newfolder(name='GSM')
umts_folder_avrupa = kml_avrupa.newfolder(name='UMTS')
lte_folder_avrupa = kml_avrupa.newfolder(name='LTE')

dic_gsm = {}
dic_umts = {}
dic_lte = {}

for i in avrupa_list:
    dic_site[i] = site_folder_avrupa.newfolder()
    dic_site[i].name = i
    dic_gsm[i] = gsm_folder_avrupa.newfolder()
    dic_gsm[i].name = i
    dic_umts[i] = umts_folder_avrupa.newfolder()
    dic_umts[i].name = i
    dic_lte[i] =  lte_folder_avrupa.newfolder()
    dic_lte[i].name  = i

# SITE KISMI
for siteid in SITEDICT.keys():
    city = SITEDICT[siteid][4]
    if city in avrupa_list:
        lat = SITEDICT[siteid][1]
        lon = SITEDICT[siteid][2]
        site_name = SITEDICT[siteid][0]
        pnt = dic_site[city].newpoint(name=site_name, coords=[(lon, lat)])
        pnt.style.labelstyle.scale = 0.7
        pnt.iconstyle.scale = 0.5
        pnt.iconstyle.color = 'ff0000ff'
        pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'

####GSM KISMI
# CELLNAME	CITY	DISTRICT	REGION	SITE_NAME	Site_ID	LAC	CI	BCCHNO	NCC	BCC	BSC
# Lat_Site	Lon_Site	AZIMUTH	M_TILT	E_TILT	HEIGHT	TRX_NUM
for cellname in cellnameListGSM:
    city = GSMDict["CITY"][cellname]
    district = GSMDict["DISTRICT"][cellname]
    if district in avrupa_list:
    #if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = GSMDict["Lat_Site"][cellname]
        lon = GSMDict["Lon_Site"][cellname]
        azimuth = GSMDict["AZIMUTH"][cellname]
        beam = techSytle["GSM"]["beam"]
        outer_ind = techSytle["GSM"]["outer_ind"]
        inner_ind = techSytle["GSM"]["inner_ind"]
        radius = techSytle["GSM"]["outer"]
        d1 = getEndpoint(lat,lon,azimuth,radius)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,radius)
        site = GSMDict["SITE_NAME"][cellname]
        antenna = ""
        height = GSMDict["HEIGHT"][cellname]
        lac = GSMDict["LAC"][cellname]
        bcch = GSMDict["BCCHNO"][cellname]
        bsc = GSMDict["BSC"][cellname]

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            gsm_cell = dic_gsm[district].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(), outerboundaryis=indoor_outer.to_kml())
            gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
            gsm_cell.extrude = 1
            gsm_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            gsm_cell = dic_gsm[district].newpolygon(name=cellname)
            gsm_cell.outerboundaryis = [(lon,lat,h), (d1[1],d1[0],h),(d2[1],d2[0],h),(lon,lat,h)]
            gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.width = cellwidth
            gsm_cell.extrude = 1
            gsm_cell.fill = 1
            gsm_cell.outline = 1
            gsm_cell.altitudemode = simplekml.AltitudeMode.relativetoground
            gsm_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

####UMTS KISMI
#CELLNAME	SectorWithNodeBName	DC_Freqs	DC_Stat	DC_Cells	Sector	Site_ID	REGION	City	DISTRICT	NODEBNAME	NODEBID	CELLID
#LOCELL	BANDIND	UARFCNDOWNLINK	DL_Freq	UARFCNUPLINK	LAC	SAC	RAC	PSCRAMBCODE	TCELL	CIO	SPGID	ACTSTATUS	BLKSTATUS
# Lat_Site	Lon_Site	RNCNAME	AZIMUTH	M_TILT	E_TILT	HEIGHT	ANTENNA	CELLTYPE	RNCID	Strategy1	Comment
for cellname in cellnameListUMTS:
    city = UMTSDict["City"][cellname]
    district = UMTSDict["DISTRICT"][cellname]
    if district in avrupa_list:
    #if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = UMTSDict["Lat_Site"][cellname]
        lon = UMTSDict["Lon_Site"][cellname]
        azimuth = UMTSDict["AZIMUTH"][cellname]
        beam = techSytle["UMTS"]["beam"]
        radius = techSytle["UMTS"]["outer"]
        outer_ind = techSytle["UMTS"]["outer_ind"]
        inner_ind = techSytle["UMTS"]["inner_ind"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,radius)
        d2 = getEndpoint(lat,lon,azimuth,radius)
        site = UMTSDict["NODEBNAME"][cellname]
        antenna = UMTSDict["ANTENNA"][cellname]
        height = UMTSDict["HEIGHT"][cellname]
        lac = UMTSDict["LAC"][cellname]
        bcch = UMTSDict["PSCRAMBCODE"][cellname]
        bsc = UMTSDict["RNCNAME"][cellname]

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            umts_cell = dic_umts[district].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(),outerboundaryis=indoor_outer.to_kml())
            umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
            umts_cell.extrude = 1
            umts_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            umts_cell = dic_umts[district].newpolygon(name=cellname)
            umts_cell.outerboundaryis = [(lon,lat,h), (d1[1],d1[0],h),(d2[1],d2[0],h),(lon,lat,h)]
            umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.width = cellwidth
            umts_cell.extrude = 1
            umts_cell.fill = 1
            umts_cell.outline = 1
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
    district = LTEDict["DISTRICT"][cellname]
    if district in avrupa_list:
    #if city == "EDIRNE" or city == "ISTANBUL" or city == "KIRKLARELI" or city == "TEKIRDAG":
        band = str(LTEDict["DLEARFCN"][cellname])
        lat = LTEDict["Lat_Site"][cellname]
        lon = LTEDict["Lon_Site"][cellname]
        azimuth = LTEDict["AZIMUTH"][cellname]
        beam = techSytle[band]["beam"]
        outer = techSytle[band]["outer"]
        outer_ind = techSytle[band]["outer_ind"]
        inner_ind = techSytle[band]["inner_ind"]
        inner = techSytle[band]["inner"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,outer)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,outer)
        d0 = getEndpoint(lat,lon,azimuth + beam/2,inner)
        d4 = getEndpoint(lat,lon,azimuth - beam/2,inner)
        midin = getEndpoint(lat, lon, azimuth, inner + 0.002)
        midout = getEndpoint(lat, lon, azimuth, outer + 0.002)
        site = LTEDict["EnodebName"][cellname]
        antenna = LTEDict["ANTENNA"][cellname]
        height = LTEDict["HEIGHT"][cellname]
        lac = LTEDict["TAC"][cellname]
        bcch = LTEDict["PHYCELLID"][cellname]
        bsc = ""

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            lte_cell = dic_lte[district].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(),
                                            outerboundaryis=indoor_outer.to_kml())
            lte_cell.style.polystyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.color = techSytle[band]["color"]
            lte_cell.extrude = 1
            lte_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            lte_cell = dic_lte[district].newpolygon(name=cellname)
            lte_cell.outerboundaryis = [(d0[1],d0[0],h), (d1[1],d1[0],h),(midout[1],midout[0],h),(d2[1],d2[0],h),(d4[1],d4[0],h),(midin[1],midin[0],h),(d0[1],d0[0],h)]
            lte_cell.style.polystyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.width = cellwidth
            lte_cell.extrude = 1
            lte_cell.fill = 1
            lte_cell.outline = 1
            lte_cell.altitudemode = simplekml.AltitudeMode.relativetoground
            lte_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

kml_avrupa.savekmz("AVRUPA.kmz",False)


'''
ASYA
'''

kml_asya = simplekml.Kml()
site_folder_asya = kml_asya.newfolder(name='Site')
gsm_folder_asya = kml_asya.newfolder(name='GSM')
umts_folder_asya = kml_asya.newfolder(name='UMTS')
lte_folder_asya = kml_asya.newfolder(name='LTE')
site_folder_asya.visibility = 0
dic_gsm = {}
dic_umts = {}
dic_lte = {}
for i in asya_list:
    dic_site[i] = site_folder_asya.newfolder()
    dic_site[i].name = i
    dic_gsm[i] = gsm_folder_asya.newfolder()
    dic_gsm[i].name = i
    dic_umts[i] = umts_folder_asya.newfolder()
    dic_umts[i].name = i
    dic_lte[i] =  lte_folder_asya.newfolder()
    dic_lte[i].name  = i

# SITE KISMI
for siteid in SITEDICT.keys():
    city = SITEDICT[siteid][4]
    if city in asya_list:
        lat = SITEDICT[siteid][1]
        lon = SITEDICT[siteid][2]
        site_name = SITEDICT[siteid][0]
        pnt = dic_site[city].newpoint(name=site_name, coords=[(lon, lat)])
        pnt.style.labelstyle.scale = 0.7
        pnt.iconstyle.scale = 0.5
        pnt.iconstyle.color = 'ff0000ff'
        pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'

####GSM KISMI
# CELLNAME	CITY	DISTRICT	REGION	SITE_NAME	Site_ID	LAC	CI	BCCHNO	NCC	BCC	BSC
# Lat_Site	Lon_Site	AZIMUTH	M_TILT	E_TILT	HEIGHT	TRX_NUM
for cellname in cellnameListGSM:
    city = GSMDict["CITY"][cellname]
    district = GSMDict["DISTRICT"][cellname]
    if district in asya_list:
    #if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = GSMDict["Lat_Site"][cellname]
        lon = GSMDict["Lon_Site"][cellname]
        azimuth = GSMDict["AZIMUTH"][cellname]
        beam = techSytle["GSM"]["beam"]
        outer_ind = techSytle["GSM"]["outer_ind"]
        inner_ind = techSytle["GSM"]["inner_ind"]
        radius = techSytle["GSM"]["outer"]
        d1 = getEndpoint(lat,lon,azimuth,radius)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,radius)
        site = GSMDict["SITE_NAME"][cellname]
        antenna = ""
        height = GSMDict["HEIGHT"][cellname]
        lac = GSMDict["LAC"][cellname]
        bcch = GSMDict["BCCHNO"][cellname]
        bsc = GSMDict["BSC"][cellname]

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            gsm_cell = dic_gsm[district].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(), outerboundaryis=indoor_outer.to_kml())
            gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
            gsm_cell.extrude = 1
            gsm_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:

            gsm_cell = dic_gsm[district].newpolygon(name=cellname)
            gsm_cell.outerboundaryis = [(lon,lat,h), (d1[1],d1[0],h),(d2[1],d2[0],h),(lon,lat,h)]
            gsm_cell.style.polystyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.color = techSytle["GSM"]["color"]
            gsm_cell.style.linestyle.width = cellwidth
            gsm_cell.extrude = 1
            gsm_cell.fill = 1
            gsm_cell.outline = 1
            gsm_cell.altitudemode = simplekml.AltitudeMode.relativetoground
            gsm_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

####UMTS KISMI
#CELLNAME	SectorWithNodeBName	DC_Freqs	DC_Stat	DC_Cells	Sector	Site_ID	REGION	City	DISTRICT	NODEBNAME	NODEBID	CELLID
#LOCELL	BANDIND	UARFCNDOWNLINK	DL_Freq	UARFCNUPLINK	LAC	SAC	RAC	PSCRAMBCODE	TCELL	CIO	SPGID	ACTSTATUS	BLKSTATUS
# Lat_Site	Lon_Site	RNCNAME	AZIMUTH	M_TILT	E_TILT	HEIGHT	ANTENNA	CELLTYPE	RNCID	Strategy1	Comment
for cellname in cellnameListUMTS:
    city = UMTSDict["City"][cellname]
    district = UMTSDict["DISTRICT"][cellname]
    if district in asya_list:
    #if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = UMTSDict["Lat_Site"][cellname]
        lon = UMTSDict["Lon_Site"][cellname]
        azimuth = UMTSDict["AZIMUTH"][cellname]
        beam = techSytle["UMTS"]["beam"]
        radius = techSytle["UMTS"]["outer"]
        outer_ind = techSytle["UMTS"]["outer_ind"]
        inner_ind = techSytle["UMTS"]["inner_ind"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,radius)
        d2 = getEndpoint(lat,lon,azimuth,radius)
        site = UMTSDict["NODEBNAME"][cellname]
        antenna = UMTSDict["ANTENNA"][cellname]
        height = UMTSDict["HEIGHT"][cellname]
        lac = UMTSDict["LAC"][cellname]
        bcch = UMTSDict["PSCRAMBCODE"][cellname]
        bsc = UMTSDict["RNCNAME"][cellname]

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            umts_cell = dic_umts[district].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(),
                                                  outerboundaryis=indoor_outer.to_kml())
            umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
            umts_cell.extrude = 1
            umts_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            umts_cell = dic_umts[district].newpolygon(name=cellname)
            umts_cell.outerboundaryis = [(lon,lat,h), (d1[1],d1[0],h),(d2[1],d2[0],h),(lon,lat,h)]
            umts_cell.style.polystyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.color = techSytle["UMTS"]["color"]
            umts_cell.style.linestyle.width = cellwidth
            umts_cell.extrude = 1
            umts_cell.fill = 1
            umts_cell.outline = 1
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
    district = LTEDict["DISTRICT"][cellname]
    if district in asya_list:
    #if city == "EDIRNE" or city == "ISTANBUL" or city == "KIRKLARELI" or city == "TEKIRDAG":
        band = str(LTEDict["DLEARFCN"][cellname])
        lat = LTEDict["Lat_Site"][cellname]
        lon = LTEDict["Lon_Site"][cellname]
        azimuth = LTEDict["AZIMUTH"][cellname]
        beam = techSytle[band]["beam"]
        outer = techSytle[band]["outer"]
        inner = techSytle[band]["inner"]
        outer_ind = techSytle[band]["outer_ind"]
        inner_ind = techSytle[band]["inner_ind"]
        d1 = getEndpoint(lat,lon,azimuth + beam/2,outer)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,outer)
        d0 = getEndpoint(lat,lon,azimuth + beam/2,inner)
        d4 = getEndpoint(lat,lon,azimuth - beam/2,inner)
        midin = getEndpoint(lat, lon, azimuth, inner + 0.002)
        midout = getEndpoint(lat, lon, azimuth, outer + 0.002)
        site = LTEDict["EnodebName"][cellname]
        antenna = LTEDict["ANTENNA"][cellname]
        height = LTEDict["HEIGHT"][cellname]
        lac = LTEDict["TAC"][cellname]
        bcch = LTEDict["PHYCELLID"][cellname]
        bsc = ""

        if ('I' in cellname):

            indoor_outer = polycircles.Polycircle(latitude=lat, longitude=lon, radius=outer_ind, number_of_vertices=36)
            indoor_inner = polycircles.Polycircle(latitude=lat, longitude=lon, radius=inner_ind, number_of_vertices=36)
            lte_cell = dic_lte[district].newpolygon(name=cellname, innerboundaryis=indoor_inner.to_kml(),
                                                outerboundaryis=indoor_outer.to_kml())
            lte_cell.style.polystyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.color = techSytle[band]["color"]
            lte_cell.extrude = 1
            lte_cell.description = descript(cellname, site, antenna, azimuth, height, lac, bcch, bsc)

        else:
            lte_cell = dic_lte[district].newpolygon(name=cellname)
            lte_cell.outerboundaryis = [(d0[1],d0[0],h), (d1[1],d1[0],h),(midout[1],midout[0],h),(d2[1],d2[0],h),(d4[1],d4[0],h),(midin[1],midin[0],h),(d0[1],d0[0],h)]
            lte_cell.style.polystyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.color = techSytle[band]["color"]
            lte_cell.style.linestyle.width = cellwidth
            lte_cell.extrude = 1
            lte_cell.fill = 1
            lte_cell.outline = 1
            lte_cell.altitudemode = simplekml.AltitudeMode.relativetoground
            lte_cell.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

kml_asya.savekmz("ASYA.kmz",False)