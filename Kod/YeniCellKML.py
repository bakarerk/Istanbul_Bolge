from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import simplekml

def getEndpoint(lat1, lon1, bearing, d):
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, d * 1852.0)
    return d['lat2'], d['lon2']

lat = 41.091893
lon = 26.548341

d1 = getEndpoint(lat,lon,10,0.4)
d2 = getEndpoint(lat,lon,-10,0.4)
print(d1)
print(d2)

kml = simplekml.Kml()
pol = kml.newpolygon(name='A Polygon')
pol.outerboundaryis = [(lon,lat), (d1[1],d1[0]),
                       (d2[1],d2[0]),(lon,lat)]
pol.style.linestyle.color = simplekml.Color.green
pol.style.linestyle.width = 5
pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
kml.save("Polygon Styling.kml")