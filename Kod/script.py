#!/usr/bin/env python
# coding: utf-8

# In[1]:


import simplekml
import os
import sys
from pygc import great_circle
import pandas as pd
import numpy as np
from polycircles import polycircles


# In[ ]:


'''geo_list = []

for index, row in site_df.iloc[:100].iterrows():
    lon = row['Longitude']
    lat = row['Latitude']
    
    location = geocoder.reverse((lat, lon))
    
  #  tup = (location['address']['town'], location['address']['suburb'])
    print(index)

    
    geo_list.append(location.raw['address'])
    
geocoder = Nominatim(user_agent = 'your_app_name')
location = geocoder.reverse((41.01391, ))
nom=location.raw
nom['address'] '''


# In[66]:


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


# In[67]:


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


# In[68]:


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


# In[69]:


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


# In[70]:


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


# ## Import Atoll DB

# In[2]:


atoll_file = sys.argv[1]


# In[7]:


#site_df = pd.read_excel('Atoll_Export_09122020.xlsx', sheet_name='Site')
site_df = pd.read_excel(atoll_file, sheet_name='Site')
#site_df.head()


# In[8]:


#gsm_df = pd.read_excel('Atoll_Export_09122020.xlsx', sheet_name='GSM')
gsm_df = pd.read_excel(atoll_file, sheet_name='GSM')
#gsm_df.head()


# In[9]:


#umts_df = pd.read_excel('Atoll_Export_09122020.xlsx', sheet_name='UMTS')
umts_df = pd.read_excel(atoll_file, sheet_name='UMTS')


# In[10]:


#umts_cell_df = pd.read_excel('Atoll_Export_09122020.xlsx', sheet_name='UMTS_CELL')
umts_cell_df = pd.read_excel(atoll_file, sheet_name='UMTS_CELL')


# In[11]:


#lte_df = pd.read_excel('Atoll_Export_09122020.xlsx', sheet_name='LTE')
lte_df = pd.read_excel(atoll_file, sheet_name='LTE')


# In[12]:


#lte_cell_df = pd.read_excel('Atoll_Export_09122020.xlsx', sheet_name='LTE_CELL')
lte_cell_df = pd.read_excel(atoll_file, sheet_name='LTE_CELL')


# In[91]:


avrupa_list = {'BEYLIKDUZU', 'BAKIRKOY', 'BESIKTAS', 'FATIH', 'EYUP', 'GAZIOSMANPASA', 'BEYOGLU',
             'KAGITHANE', 'SARIYER', 'ZEYTINBURNU', 'SISLI', 'KUCUKCEKMECE',  'CATALCA',
              'AVCILAR', 'SILIVRI','BAHCELIEVLER', 'ESENYURT', 'ARNAVUTKOY', 'BUYUKCEKMECE',
       'BAGCILAR', 'BASAKSEHIR', 'ESENLER', 'BAYRAMPASA', 'GUNGOREN','SULTANGAZI'}
asya_list = {'KADIKOY', 'USKUDAR', 'TUZLA', 'SANCAKTEPE', 'BEYKOZ', 'CEKMEKOY', 'PENDIK', 'KARTAL',
             'MALTEPE', 'UMRANIYE','SILE', 'ATASEHIR', 'ADALAR', 'SULTANBEYLI'}
trakya_list = {'TEKIRDAG','EDIRNE','KIRKLARELI'}

avrupa_camera = [41.056352, 28.915095, 23378, 3.000000, 15.000000]
asya_camera = [41.033368,  29.261240, 41670, -1.000000, 6.000000]
trakya_camera = [41.362845, 26.938775, 260711, -3.000000, 6.000000]

#camera = asya_camera
#camera = avrupa_camera
camera = trakya_camera

#site_sub = site_df[site_df['DISTRICT'].isin(asya_list)] # ASYA
#site_sub = site_df[site_df['DISTRICT'].isin(avrupa_list)] # AVRUPA
site_sub = site_df[site_df['CITY'].isin(trakya_list)] # TRAKYA

#kml_path = "\\Users\\retter\\Desktop\\KML\\ASYA.kmz"
#kml_path = "\\Users\\retter\\Desktop\\KML\\AVRUPA.kmz"
kml_path = "\\Users\\retter\\Desktop\\Tkinter\\TRAKYA.kmz"

dic = {}
district_dic = {}
dic_gsm = {}
district_dic_gsm = {}
dic_umts = {}
district_dic_umts = {}
dic_lte = {}
district_dic_lte = {}
avrupa_dic = {}
asya_dic = {}
trakya_dic = {}



kml = simplekml.Kml()
site_folder = kml.newdocument(name='Site')
site_folder.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
site_folder.lookat.latitude = camera[0]
site_folder.lookat.longitude = camera[1]
site_folder.lookat.range = camera[2]
site_folder.lookat.heading = camera[3]
site_folder.lookat.tilt = camera[4]
#site_folder.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
gsm_folder = kml.newdocument(name='GSM')
umts_folder = kml.newdocument(name='UMTS')
lte_folder = kml.newdocument(name='LTE')


for city in site_sub['CITY'].unique():
    dic[city] = site_folder.newfolder()
    dic[city].name = city
    dic_gsm[city] = gsm_folder.newfolder()
    dic_gsm[city].name = city
    dic_umts[city] = umts_folder.newfolder()
    dic_umts[city].name = city
    dic_lte[city] = lte_folder.newfolder()
    dic_lte[city].name = city
    
    for district in site_sub[site_sub['CITY']==city]['DISTRICT'].unique():
            
        district_dic[district] = dic[city].newfolder()
        district_dic[district].name = district
        district_dic_gsm[district] = dic_gsm[city].newfolder()
        district_dic_gsm[district].name = district
        district_dic_umts[district] = dic_umts[city].newfolder()
        district_dic_umts[district].name = district
        district_dic_lte[district] = dic_lte[city].newfolder()
        district_dic_lte[district].name = district
        
        
'''

for district in site_sub[site_sub['CITY']=='ISTANBUL']['DISTRICT'].unique():
            
        district_dic[district] = site_folder.newfolder()
        district_dic[district].name = district
        
        district_dic_gsm[district] = gsm_folder.newfolder()
        district_dic_gsm[district].name = district
        district_dic_umts[district] = umts_folder.newfolder()
        district_dic_umts[district].name = district
        district_dic_lte[district] = lte_folder.newfolder()
        district_dic_lte[district].name = district
        

'''
coeff = 0.7
site_sub = site_sub.replace(np.nan, '', regex=True)
gsm_df = gsm_df.replace(np.nan, '', regex=True)
umts_df = umts_df.replace(np.nan, '', regex=True)
umts_cell_df = umts_cell_df.replace(np.nan, '', regex=True)
lte_df = lte_df.replace(np.nan, '', regex=True)
lte_cell_df = lte_cell_df.replace(np.nan, '', regex=True)

style_site = simplekml.Style()
style_site.iconstyle.color = 'ff0000ff'
style_site.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'

style_linestring = simplekml.Style()
style_linestring.linestyle.width = 1*coeff
style_linestring.linestyle.color = '88ff5500'
style_linestring.polystyle.color = '88ff5500'

style_linestring_dx_dy = simplekml.Style()
style_linestring_dx_dy.linestyle.width = 4*coeff
style_linestring_dx_dy.linestyle.color = 'ff381e33'

style_site_sml_normal = simplekml.Style()
style_site_sml_normal.iconstyle.scale=0.7
style_site_sml_normal.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
style_site_sml_normal.labelstyle.scale = 0

style_site_sml_highlight = simplekml.Style()
style_site_sml_highlight.iconstyle.scale=1.2
style_site_sml_highlight.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
style_site_sml_highlight.labelstyle.scale = 1
  
stylemap_sml = simplekml.StyleMap()
stylemap_sml.normalstyle = style_site_sml_normal
stylemap_sml.highlightstyle = style_site_sml_highlight

style_site_normal = simplekml.Style()
style_site_normal.iconstyle.scale=0.7
style_site_normal.iconstyle.color = 'ff0000ff'
style_site_normal.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
style_site_normal.labelstyle.scale = 0

style_site_highlight = simplekml.Style()
style_site_highlight.iconstyle.scale=1.2
style_site_highlight.iconstyle.color = 'ff0000ff'
style_site_highlight.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
style_site_highlight.labelstyle.scale = 1
  
stylemap = simplekml.StyleMap()
stylemap.normalstyle = style_site_normal
stylemap.highlightstyle = style_site_highlight

style_site_normal_repeater = simplekml.Style()
style_site_normal_repeater.iconstyle.scale=0.7
style_site_normal_repeater.iconstyle.color = 'ff14F0F0'
style_site_normal_repeater.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/triangle.png'
style_site_normal_repeater.labelstyle.scale = 0

style_site_highlight_repeater = simplekml.Style()
style_site_highlight_repeater.iconstyle.scale=1.2
style_site_highlight_repeater.iconstyle.color = 'ff14F0F0'
style_site_highlight_repeater.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/triangle.png'
style_site_highlight_repeater.labelstyle.scale = 1
  
stylemap_repeater = simplekml.StyleMap()
stylemap_repeater.normalstyle = style_site_normal_repeater
stylemap_repeater.highlightstyle = style_site_highlight_repeater

style_band_3 = simplekml.Style()
style_band_3.linestyle.color = '85ff5500'
style_band_3.polystyle.color = '85ff5500'

style_band_5 = simplekml.Style()
style_band_5.linestyle.color = '85f69b45'
style_band_5.polystyle.color = '85f69b45'

style_band_7 = simplekml.Style()
style_band_7.linestyle.color = '85ff00aa'
style_band_7.polystyle.color = '85ff00aa'

style_band_8 = simplekml.Style()
style_band_8.linestyle.color = '850095e5'
style_band_8.polystyle.color = '850095e5'

style_band_1 = simplekml.Style()
style_band_1.linestyle.color = '85381e33'
style_band_1.polystyle.color = '85381e33'

band_dict = {'3': style_band_3, '5': style_band_5, '7': style_band_7, '8': style_band_8, '1': style_band_1,
            '2': style_band_1, '4': style_band_1, '6': style_band_1, '9': style_band_1}

style_umts = simplekml.Style()
style_gsm = simplekml.Style()

style_umts.linestyle.color = "851f03a4"
style_umts.polystyle.color = "851f03a4"
style_gsm.linestyle.color = "9864b736"
style_gsm.polystyle.color = "9864b736"

#for i in range(10):
for i in range(len(site_sub)):
    site = site_sub.iloc[i]
    
    #if(site['Name']!='Y6829'):
     #   continue
        
    cell_count = 0
    
    lon = str(site['Longitude'])[:9]
    lat = str(site['Latitude'])[:9]
    site_name = site['SITE_NAME']
    site_name_3g = site['SITE_NAME_3G']
    site_name_4g = site['SITE_NAME_4G']
    construction_type = site['CONSTRUCTION_TYPE']
    construction_height = str(site['CONSTRUCTION_HEIGHT'])
    equipment = site['Equipment']
    district = site['DISTRICT']
    north = float(lat) + (180/np.pi)*(10/6378137)
    east = float(lon) + (180/np.pi)*(10/6378137)
    south = float(lat) - (180/np.pi)*(10/6378137)
    west = float(lon) - (180/np.pi)*(10/6378137)
    north_dx_dy = float(lat) + (180/np.pi)*(10/6378137)
    east_dx_dy = float(lon) + (180/np.pi)*(10/6378137)
    south_dx_dy = float(lat) - (180/np.pi)*(10/6378137)
    west_dx_dy = float(lon) - (180/np.pi)*(10/6378137)
    site_address = site['SITE_ADDRESS']
    
    
    
    lod = simplekml.Lod(minlodpixels=7)
    latlonbox = simplekml.LatLonBox(east=east, north=north, south=south,west=west)
    latlonbox_dx_dy = simplekml.LatLonBox(east=east_dx_dy, north=north_dx_dy, south=south_dx_dy,west=west_dx_dy)
    region = simplekml.Region(latlonbox, lod)
    region_dx_dy = simplekml.Region(latlonbox_dx_dy, lod)
    
    lod_medium = simplekml.Lod(minlodpixels=3)
    region_medium = simplekml.Region(latlonbox, lod_medium)
    
    pnt = district_dic[district].newpoint(name=site_name,coords = [(lon , lat)]) 
      
    for index,row in gsm_df[gsm_df['Site']==site['Name']].iterrows():
        
        region_gsm = region
        
        if(row["Azimuth (°)"]==''):
            continue
        
        if('I' in str(row['OMC_CELLNAME'])):
            cell_count +=1
        
        if(str((row['LAC']))!=''):
            lac_gsm = str(int(row['LAC']))
        else:
            lac_gsm = str(row['LAC'])
            
        if(str((row['BCCH']))!=''):
            bcch = str(int(row['BCCH']))
        else:
            bcch = str(row['BCCH'])
            
        lat_2, lon_2 = get_dx_dy_coord(lat, lon, row['DX (m)'], row['DY (m)'])
        
        if(((str((row['DX (m)']))!='') | (str(row['DX (m)'])!='0')) |
           ((str((row['DY (m)']))!='') | (str(row['DY (m)'])!='0')) ):
            
            if('I' in str(row['OMC_CELLNAME'])):
                linestring = district_dic_gsm[district].newlinestring(coords=[(lon, lat, 1),(lon_2, lat_2,1)])
            else:
                linestring = district_dic_gsm[district].newlinestring(coords=[(lon, lat, 9*coeff),
                                                                              (lon_2, lat_2,9*coeff)])
            linestring.region = region
            linestring.altitudemode = 'relativeToGround'
            linestring.extrude = 1
            linestring.fill = 1
            linestring.outline = 1      
            linestring.style = style_linestring_dx_dy
            
            region_gsm = region_dx_dy
        
        
        
        gsm_poly(coeff, cell_count, style_gsm, float(lat_2), float(lon_2), int(row["Azimuth (°)"]), district_dic_gsm[district],
                 region_gsm, str(row['OMC_CELLNAME']),
                str(row['Site']), str(row['Antenna']), str(int(row['Mechanical Downtilt (°)'])),
                 str(int(row['Height (m)'])),
                lac_gsm, bcch, str(row['BSC']))
       
  
    for index,row in umts_df[umts_df['Site']==site['Name']].iterrows():
        
        region_umts = region
        
        if(row["Azimuth (°)"]==''):
            continue
            
        #if('I' in str(umts_cell['OMC_CELLNAME'].values[0])):    
        cell_count += 1
            
        umts_cell = umts_cell_df[umts_cell_df['Transmitter']==row['Transmitter']]
        
        if(str(row['Mechanical Downtilt (°)'])!=''):
            mtilt_umts = str(int(row['Mechanical Downtilt (°)']))
        else:
            mtilt_umts = str(row['Mechanical Downtilt (°)'])
            
        if(str(umts_cell['LAC'].values[0])!=''):
            lac_umts = str(int(umts_cell['LAC'].values[0]))
        else:
            lac_umts = str(umts_cell['LAC'].values[0])
            
        if(str(umts_cell['URA'].values[0])!=''):
            ura_umts = str(int(umts_cell['URA'].values[0]))
        else:
            ura_umts = str(umts_cell['URA'].values[0])
            
        if(str(umts_cell['Primary scrambling code'].values[0])!=''):
            psc = str(int(umts_cell['Primary scrambling code'].values[0]))
        else:
            psc = str(umts_cell['Primary scrambling code'].values[0])
            
        lat_2, lon_2 = get_dx_dy_coord(lat, lon, row['DX (m)'], row['DY (m)'])
        
        if(((str((row['DX (m)']))!='') | (str(row['DX (m)'])!='0')) |
           ((str((row['DY (m)']))!='') | (str(row['DY (m)'])!='0')) ):
            
            if('I' in str(umts_cell['OMC_CELLNAME'].values[0])):
                linestring = district_dic_umts[district].newlinestring(coords=[(lon, lat, 1),(lon_2, lat_2,1)])
            else:
                linestring = district_dic_umts[district].newlinestring(coords=[(lon, lat, 9*coeff),
                                                                               (lon_2, lat_2,9*coeff)])
        
            linestring.region = region
            linestring.altitudemode = 'relativeToGround'
            linestring.extrude = 1
            linestring.fill = 1
            linestring.outline = 1
            linestring.style = style_linestring_dx_dy
            
            region_umts = region_dx_dy
       
        umts_poly(coeff, cell_count, style_umts, float(lat_2), float(lon_2), int(row["Azimuth (°)"]), district_dic_umts[district], region_umts, 
                  str(umts_cell['OMC_CELLNAME'].values[0]),
                str(row['Site']), str(row['Antenna']), mtilt_umts, 
                  str(int(row['Height (m)'])),
                str(row['SECTOR_TYPE']), str(umts_cell['RNC'].values[0]), lac_umts,
                  ura_umts,psc,str(str(umts_cell['Max Power (dBm)'].values[0])+" - "+
                                  str(umts_cell['Pilot Power (dBm)'].values[0])))
        
    lte_band_check = 0
    previous_cell_id = 100
    for index,row in lte_df[lte_df['Site']==site['Name']].sort_values(by=['Transmitter']).iterrows():
        
        region_lte = region 

        if(row["Azimuth (°)"]==''):
            continue
            
       
        cell_count += 1
            
        lte_cell = lte_cell_df[lte_cell_df['Transmitter']==row['Transmitter']]
        
        if(str(lte_cell['TAC'].values[0])!=''):
            tac_lte = str(int(lte_cell['TAC'].values[0]))
        else:
            tac_lte = str(lte_cell['TAC'].values[0])
            
        if(str(row['Mechanical Downtilt (°)'])!=''):
            mtilt_lte = str(int(row['Mechanical Downtilt (°)']))
        else:
            mtilt_lte = str(row['Mechanical Downtilt (°)'])
            
        if(str(lte_cell['Physical Cell ID'].values[0])!=''):
            pci_lte = str(int(lte_cell['Physical Cell ID'].values[0]))
        else:
            pci_lte = str(lte_cell['Physical Cell ID'].values[0])
        
        if(int(str(row['Transmitter'])[-2]) != previous_cell_id):
            lte_band_check+=1
            
        lat_2, lon_2 = get_dx_dy_coord(lat, lon, row['DX (m)'], row['DY (m)'])
        
        if(((str((row['DX (m)']))!='') | (str(row['DX (m)'])!='0')) |
           ((str((row['DY (m)']))!='') | (str(row['DY (m)'])!='0')) ):
            
            if('I' in str(lte_cell['OMC_CELLNAME'].values[0])):
                linestring = district_dic_lte[district].newlinestring(coords=[(lon, lat, 1),(lon_2, lat_2,1)])
            else:
                linestring = district_dic_lte[district].newlinestring(coords=[(lon, lat, 9*coeff),
                                                                              (lon_2, lat_2,9*coeff)])
            
            linestring.region = region
            linestring.altitudemode = 'relativeToGround'
            linestring.extrude = 1
            linestring.fill = 1
            linestring.outline = 1
            
            
            linestring.style = style_linestring_dx_dy
            
            region_lte = region_dx_dy
        
        lte_poly(coeff, cell_count, style_linestring, lte_band_check, band_dict[str(row['Transmitter'])[-2]], float(lat_2), float(lon_2),
                 int(row["Azimuth (°)"]), district_dic_lte[district], region_lte, 
                  str(lte_cell['OMC_CELLNAME'].values[0]),
                str(row['Site']), str(row['Antenna']), mtilt_lte, 
                  str(int(row['Height (m)'])),
                 tac_lte,
                 str(row['Transmitter'])[:-2],   #enodebid
                 str(hex(int(int(str(row['Transmitter'])[:-2])*256 + int(str(row['Transmitter'])[-2:]))))[2:], #ECI
                  pci_lte,
                  str(str(lte_cell['Max Power (dBm)'].values[0])+" - "+
                      str(lte_cell['RS EPRE per antenna port (dBm)'].values[0])))
        
        previous_cell_id = int(str(row['Transmitter'])[-2])        

    pnt.region = region_medium
   
    pnt.description = '''

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
        <th>SITE NAME</th>
        <td>'''+str(site_name)+'''</td>
      </tr>
      <tr>
        <th>SITE NAME 3G</th>
         <td>'''+str(site_name_3g)+'''</td>
      </tr>
      <tr>
        <th>SITE NAME 4G</th>
         <td>'''+str(site_name_4g)+'''</td>
      </tr>
      <tr>
        <th>Lat // Lon </th>
         <td>'''+str(lat)+''' // '''+str(lon)+'''</td>
      </tr>
      <tr>
        <th>CONSTRUCTION TYPE</th>
         <td>'''+str(construction_type)+'''</td>
      </tr>
      <tr>
        <th>CONSTRUCTION HEIGHT</th>
         <td>'''+str(construction_height)+'''</td>
      </tr>
      <tr>
        <th>EQUIPMENT</th>
         <td>'''+str(equipment)+'''</td>
      </tr>
      <tr>
        <th>DISTRICT</th>
         <td>'''+str(district)+'''</td>
      </tr>
     <tr>
        <th>SITE ADDRESS</th>
         <td>'''+str(site_address)+'''</td>
      </tr>
    
    </table>

    '''
    
    if(equipment=='REPEATER'):
        pnt.stylemap = stylemap_repeater
    else:
        pnt.stylemap = stylemap
    
    lod_sml = simplekml.Lod(maxlodpixels=3, minlodpixels=0.5)
    region_sml = simplekml.Region(latlonbox, lod_sml)
    
    if(equipment!='REPEATER'):
        pnt_sml = district_dic[district].newpoint(name=site_name, coords = [(lon , lat)])
        pnt_sml.region = region_sml
        pnt_sml.stylemap = stylemap_sml
    
    
kml.savekmz(kml_path, False)  # KML PATH
os.startfile(kml_path)

