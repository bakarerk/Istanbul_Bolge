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

path  = '/LibraryFiles/'
filename_1 = 'GSM_Engineering_CellDB.xls'
#filename_2 = 'UMTS_Engineering_CellDB.xls'
#filename_3 = 'LTE_Engineering_CellDB.xls'
ftp = ftplib.FTP("gmp2kaydemir")
ftp.login("opti", "optik")
ftp.cwd(path)
ftp.retrbinary("RETR " + filename_1 ,open(filename_1, 'wb').write)
#ftp.retrbinary("RETR " + filename_2 ,open(filename_2, 'wb').write)
#ftp.retrbinary("RETR " + filename_3 ,open(filename_3, 'wb').write)
ftp.quit()

#LTE = pd.read_csv("LTE_Engineering_CellDB.xls",sep="\t")
#UMTS = pd.read_csv("UMTS_Engineering_CellDB.xls",sep="\t")
GSM = pd.read_csv("GSM_Engineering_CellDB.xls",sep="\t",low_memory=False,index_col="CELLNAME")
GSMDict = GSM.to_dict()
#CELLNAME	CITY	DISTRICT	REGION	SITE_NAME	Site_ID	LAC	CI	BCCHNO	NCC	BCC	BSC	Lat_Site	Lon_Site	AZIMUTH	M_TILT	E_TILT	HEIGHT	TRX_NUM

#cellname[9:11]

#cellnameList = ["G0112220O3411222","G0112210O3411221","G0112230O3411223"]
cellnameList = list(GSM.index)
kml = simplekml.Kml()
for cellname in cellnameList:
    city = GSMDict["CITY"][cellname]
    if city == "ISTANBUL" or city == "EDIRNE" or city == "KIRKLARELI" or city == "TEKIRDAG":
        lat = GSMDict["Lat_Site"][cellname]
        lon = GSMDict["Lon_Site"][cellname]
        azimuth = GSMDict["AZIMUTH"][cellname]
        beam = 20
        radius = 0.15
        d1 = getEndpoint(lat,lon,azimuth + beam/2,radius)
        d2 = getEndpoint(lat,lon,azimuth - beam/2,radius)
        site = GSMDict["SITE_NAME"][cellname]
        antenna = ""
        height = GSMDict["HEIGHT"][cellname]
        lac = GSMDict["LAC"][cellname]
        bcch = GSMDict["BCCHNO"][cellname]
        bsc = GSMDict["BSC"][cellname]

        pol = kml.newpolygon(name=site)
        pol.outerboundaryis = [(lon,lat), (d1[1],d1[0]),(d2[1],d2[0]),(lon,lat)]
        pol.style.polystyle.color = '850095e5'
        pol.description = descript(cellname,site,antenna,azimuth,height,lac,bcch,bsc)

kml.savekmz("Polygon Styling.kmz")

#print(newDictGSM["SITE_NAME"]["GM277020O6129802"])
#for i in newDictGSM.keys():
#    print(newDictGSM[i])
