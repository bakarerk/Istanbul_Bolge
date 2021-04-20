from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import simplekml

def getEndpoint(lat1, lon1, bearing, d):
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, d * 1852.0)
    return d['lat2'], d['lon2']

def descript(cell_name,site,antenna,azimuth,mtilt,height,lactac,bcch,bsc):
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
    <td>''' + cell_name + '''</td>
  </tr>
  <tr>
    <th>Site</th>
     <td>''' + site + '''</td>
  </tr>
  <tr>
    <th>Antenna</th>
     <td>''' + antenna + '''</td>
  </tr>
  <tr>
    <th>Azimuth</th>
     <td>''' + azimuth + '''</td>
  </tr>
  <tr>
    <th>Mechanical Downtilt</th>
     <td>''' + mtilt + '''</td>
  </tr>
  <tr>
    <th>Height</th>
     <td>''' + height + '''</td>
  </tr>
  <tr>
    <th>LAC-TAC</th>
     <td>''' + lactac + '''</td>
  </tr>
  <tr>
    <th>BCCH-PSC-PCI</th>
     <td>''' + bcch + '''</td>
  </tr>
   <tr>
    <th>BSC-RNC</th>
     <td>''' + bsc + '''</td>
  </tr>

</table>

'''

lat = 41.091893
lon = 26.548341
beam = 20
radius = 0.4

d1 = getEndpoint(lat,lon,beam/2,radius)
d2 = getEndpoint(lat,lon,-beam/2,radius)
cell_name = "LTECELLA"
site ="SITEA"
antenna = "HUAWEIX123"
azimuth = "0"
mtilt = "4"
height = "20"
lac = "34123"
bcch = "123"
bsc = "BSC01"

kml = simplekml.Kml()
pol = kml.newpolygon(name=site)
pol.outerboundaryis = [(lon,lat), (d1[1],d1[0]),(d2[1],d2[0]),(lon,lat)]
pol.style.polystyle.color = '850095e5'
pol.description = descript(cell_name,site,antenna,azimuth,mtilt,height,lac,bcch,bsc)

kml.save("Polygon Styling.kml")