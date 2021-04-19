from pygc import great_circle
from polycircles import polycircles

def gsm_poly(coeff, cell_count, style_gsm, lat, lon, azimuth, kml, region, cell_name, site, antenna, mtilt, height, lac, bcch, bsc):
    
   
    if('I' in cell_name):
        
        cell_width = 5*coeff
        next_cell_distance = 1*coeff
        
        outer_radius = cell_width*cell_count + next_cell_distance*cell_count
        inner_radius = outer_radius - cell_width
        
        polycircle_outer = polycircles.Polycircle(latitude= lat,
                                          longitude= lon,
                                          radius= outer_radius,
                                          number_of_vertices= int(60*coeff))

        polycircle_inner = polycircles.Polycircle(latitude= lat,
                                          longitude= lon,
                                          radius= inner_radius,
                                          number_of_vertices= int(60*coeff))


       

        pol = kml.newpolygon(name=cell_name, innerboundaryis=polycircle_inner.to_kml(),
                              outerboundaryis=polycircle_outer.to_kml())
    
        
    else:
    
        lat_long = great_circle(distance=82*coeff, azimuth=azimuth, latitude=lat, longitude=lon)
        lat2 = lat_long['latitude']
        lon2 = lat_long['longitude']
        lat3 = great_circle(distance=65*coeff, azimuth=azimuth-15, latitude=lat, 
                            longitude=lon)['latitude']
        lon3 = great_circle(distance=65*coeff, azimuth=azimuth-15, 
                            latitude=lat, longitude=lon)['longitude']

    
        pol = kml.newpolygon(name=cell_name)
        alt = 9*coeff
    
        pol.outerboundaryis = [(lon,lat,alt), (lon2,lat2,alt),(lon3,lat3,alt),(lon,lat,alt)]
        pol.altitudemode = 'relativeToGround'
        pol.extrude = 1
        pol.fill=1
        pol.outline = 1
        
    pol.region = region
    pol.style = style_gsm
    
    pol.description = '''

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
        <td>'''+cell_name+'''</td>
      </tr>
      <tr>
        <th>Site</th>
         <td>'''+site+'''</td>
      </tr>
      <tr>
        <th>Antenna</th>
         <td>'''+antenna+'''</td>
      </tr>
      <tr>
        <th>Azimuth</th>
         <td>'''+str(azimuth)+'''</td>
      </tr>
      <tr>
        <th>Mechanical Downtilt</th>
         <td>'''+mtilt+'''</td>
      </tr>
      <tr>
        <th>Height</th>
         <td>'''+height+'''</td>
      </tr>
      <tr>
        <th>LAC</th>
         <td>'''+lac+'''</td>
      </tr>
      <tr>
        <th>BCCH</th>
         <td>'''+bcch+'''</td>
      </tr>
       <tr>
        <th>BSC</th>
         <td>'''+bsc+'''</td>
      </tr>

    </table>

    '''


def umts_poly(coeff, cell_count, style_umts, lat, lon, azimuth, kml, region, cell_name, site, antenna, mtilt, height, sector_type,
              rnc, lac, ura, psc, pcpich):
    
    if('I' in cell_name):
        
        cell_width = 5*coeff
        next_cell_distance = 1*coeff
        
        outer_radius = cell_width*cell_count + next_cell_distance*cell_count
       
        inner_radius = outer_radius - cell_width
        
        polycircle_outer = polycircles.Polycircle(latitude= lat,
                                          longitude= lon,
                                          radius= outer_radius,
                                          number_of_vertices= int(60*coeff))

        polycircle_inner = polycircles.Polycircle(latitude= lat,
                                          longitude= lon,
                                          radius= inner_radius,
                                          number_of_vertices= int(60*coeff))


       

        pol = kml.newpolygon(name=cell_name, innerboundaryis=polycircle_inner.to_kml(),
                              outerboundaryis=polycircle_outer.to_kml())
    else:
    
        lat_long = great_circle(distance=82*coeff, azimuth=azimuth, latitude=lat, longitude=lon)
        lat2 = lat_long['latitude']
        lon2 = lat_long['longitude']
        lat3 = great_circle(distance=65*coeff, azimuth=azimuth+15, latitude=lat, longitude=lon)['latitude']
        lon3 = great_circle(distance=65*coeff, azimuth=azimuth+15, latitude=lat, longitude=lon)['longitude']


        pol = kml.newpolygon(name=cell_name)
        alt = 9*coeff

        pol.outerboundaryis = [(lon,lat,alt), (lon2,lat2,alt),(lon3,lat3,alt),(lon,lat,alt)]
        pol.altitudemode = 'relativeToGround'
        pol.extrude = 1
        pol.fill=1
        pol.outline = 1
    pol.region = region
   
    
    pol.description = '''

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
        <td>'''+cell_name+'''</td>
      </tr>
      <tr>
        <th>Antenna</th>
         <td>'''+antenna+'''</td>
      </tr>
       <tr>
        <th>Height(m)</th>
         <td>'''+height+'''</td>
      </tr>
      <tr>
        <th>Azimuth</th>
         <td>'''+str(azimuth)+'''</td>
      </tr>
      <tr>
        <th>Mechanical Downtilt</th>
         <td>'''+mtilt+'''</td>
      </tr>
      <tr>
        <th>Sector Type</th>
         <td>'''+sector_type+'''</td>
      </tr>
      <tr>
        <th>RNC</th>
         <td>'''+rnc+'''</td>
      </tr>
       <tr>
        <th>LAC</th>
         <td>'''+lac+'''</td>
      </tr>
       <tr>
        <th>URA</th>
         <td>'''+ura+'''</td>
      </tr>
      <tr>
        <th>PSC</th>
         <td>'''+psc+'''</td>
      </tr>
      <tr>
        <th>Max - PCPICH Power</th>
         <td>'''+pcpich+'''</td>
      </tr>
    
    </table>

    '''
    
    pol.style = style_umts



def lte_poly_maker(coeff, band, lat, lon, alt, azimuth):
    
    if(band==1):
        dist_1, dist_2, dist_3, dist_4 = 70*coeff, 90*coeff, 110*coeff, 87*coeff
    elif(band==2):
        dist_1, dist_2, dist_3, dist_4 = 95*coeff, 115*coeff, 138*coeff, 115*coeff
    elif(band==3):
        dist_1, dist_2, dist_3, dist_4 = 120*coeff, 140*coeff, 166*coeff, 143*coeff
    elif(band==4):
        dist_1, dist_2, dist_3, dist_4 = 145*coeff, 165*coeff, 194*coeff, 171*coeff
    else:
        dist_1, dist_2, dist_3, dist_4 = 170*coeff, 190*coeff, 222*coeff, 199*coeff
        
    lat1 = great_circle(distance=dist_1, azimuth=azimuth-15, latitude=lat, longitude=lon)['latitude']
    lon1 = great_circle(distance=dist_1, azimuth=azimuth-15, latitude=lat, longitude=lon)['longitude']
    lat2 = great_circle(distance=dist_2, azimuth=azimuth-15, latitude=lat, longitude=lon)['latitude']
    lon2 = great_circle(distance=dist_2, azimuth=azimuth-15, latitude=lat, longitude=lon)['longitude']
    lat3 = great_circle(distance=dist_3, azimuth=azimuth, latitude=lat, longitude=lon)['latitude']
    lon3 = great_circle(distance=dist_3, azimuth=azimuth, latitude=lat, longitude=lon)['longitude']
    lat4 = great_circle(distance=dist_2, azimuth=azimuth+15, latitude=lat, longitude=lon)['latitude']
    lon4 = great_circle(distance=dist_2, azimuth=azimuth+15, latitude=lat, longitude=lon)['longitude']
    lat5 = great_circle(distance=dist_1, azimuth=azimuth+15, latitude=lat, longitude=lon)['latitude']
    lon5 = great_circle(distance=dist_1, azimuth=azimuth+15, latitude=lat, longitude=lon)['longitude']
    lat6 = great_circle(distance=dist_4, azimuth=azimuth, latitude=lat, longitude=lon)['latitude']
    lon6 = great_circle(distance=dist_4, azimuth=azimuth, latitude=lat, longitude=lon)['longitude']
    
    return [(lon1,lat1,alt), (lon2,lat2,alt),(lon3,lat3,alt),(lon4,lat4,alt),
(lon5,lat5,alt), (lon6,lat6,alt), (lon1,lat1,alt)]



def lte_poly(coeff, cell_count, style_linestring, lte_band_check, band_dict, lat, lon, azimuth, kml, region, cell_name, site, antenna, mtilt, height,
             tac, enodeb_id, eci, pci,
             max_rs_power):
    

    
    if('I' in cell_name):
        
        cell_width = 5*coeff
        next_cell_distance = 1*coeff
        
        outer_radius = cell_width*cell_count + next_cell_distance*cell_count
        inner_radius = outer_radius - cell_width
        
        polycircle_outer = polycircles.Polycircle(latitude= lat,
                                          longitude= lon,
                                          radius= outer_radius,
                                          number_of_vertices= int(60*coeff))

        polycircle_inner = polycircles.Polycircle(latitude= lat,
                                          longitude= lon,
                                          radius= inner_radius,
                                          number_of_vertices= int(60*coeff))


       

        pol = kml.newpolygon(name=cell_name, innerboundaryis=polycircle_inner.to_kml(),
                              outerboundaryis=polycircle_outer.to_kml())
    
    else:
        
        pol = kml.newpolygon(name=cell_name)
        alt = 9*coeff

        outerboundary = lte_poly_maker(coeff, lte_band_check, lat, lon, alt, azimuth)
        pol.outerboundaryis = outerboundary

        lon6 = outerboundary[5][0]
        lat6 = outerboundary[5][1]

        linestring = kml.newlinestring(coords=[(lon, lat, 9*coeff),(lon6, lat6,9*coeff)])

        linestring.altitudemode = 'relativeToGround'
        linestring.extrude = 1

        linestring.fill=1
        linestring.outline = 1

        linestring.style = style_linestring

        pol.altitudemode = 'relativeToGround'
        pol.extrude = 1
        linestring.region = region
        pol.fill=1
        pol.outline = 1
    
    pol.style = band_dict
    
    pol.region = region
   
    
    pol.description = '''

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
        <td>'''+cell_name+'''</td>
      </tr>
      <tr>
        <th>Antenna</th>
         <td>'''+antenna+'''</td>
      </tr>
       <tr>
        <th>Height(m)</th>
         <td>'''+height+'''</td>
      </tr>
      <tr>
        <th>Azimuth</th>
         <td>'''+str(azimuth)+'''</td>
      </tr>
      <tr>
        <th>TAC</th>
         <td>'''+tac+'''</td>
      </tr>
      <tr>
        <th>Mechanical Downtilt</th>
         <td>'''+mtilt+'''</td>
      </tr>
      <tr>
        <th>EnodeB ID</th>
         <td>'''+enodeb_id+'''</td>
      </tr>
      <tr>
        <th>ECI (hex)</th>
         <td>'''+eci+'''</td>
      </tr>
      <tr>
        <th>PCI</th>
         <td>'''+pci+'''</td>
      </tr>
      <tr>
        <th>Max - RS Power</th>
         <td>'''+str(max_rs_power)+'''</td>
      </tr>
    
    </table>

    '''


def get_dx_dy_coord(lat, lon, dx, dy):
    
    if(str(dx)==''):
        dx=0
    if(str(dy)==''):
        dy=0
        
    lat = float(lat)
    lon = float(lon)
    
    if(((float(dx)>=0) & (float(dy)>=0))):
        lat_2 = great_circle(distance=int(dy), azimuth=0, latitude=lat, longitude=lon)['latitude']
        lon_2 = great_circle(distance=int(dx), azimuth=90, latitude=lat, longitude=lon)['longitude']
    
    if(((float(dx)<=0) & (float(dy)<=0))):
        lat_2 = great_circle(distance=abs(int(dy)), azimuth=180, latitude=lat, longitude=lon)['latitude']
        lon_2 = great_circle(distance=abs(int(dx)), azimuth=270, latitude=lat, longitude=lon)['longitude']
        
    if(((float(dx)>=0) & (float(dy)<=0))):
        lat_2 = great_circle(distance=abs(int(dy)), azimuth=180, latitude=lat, longitude=lon)['latitude']
        lon_2 = great_circle(distance=abs(int(dx)), azimuth=90, latitude=lat, longitude=lon)['longitude']
        
    if(((float(dx)<=0) & (float(dy)>=0))):
        lat_2 = great_circle(distance=abs(int(dy)), azimuth=0, latitude=lat, longitude=lon)['latitude']
        lon_2 = great_circle(distance=abs(int(dx)), azimuth=270, latitude=lat, longitude=lon)['longitude']
    
    return lat_2, lon_2