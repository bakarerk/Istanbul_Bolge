#!/usr/bin/env python
# coding: utf-8

from functions import *
from styles import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd
import simplekml
import os
import numpy as np
from PIL import ImageTk, Image
from ttkthemes import ThemedTk


class MyWindow:
    def __init__(self, parent):

        self.parent = parent
        self.region= None
        self.filename = None
        self.site_df = None
        self.gsm_df = None
        self.umts_df = None
        self.umts_cell_df = None
        self.lte_df = None
        self.lte_cell_df = None
        
        self.avrupa_list = []
        self.asya_list = []
        self.trakya_list = []
        
        
        self.region_label = ttk.Label(self.parent, text='Select Region:', foreground='black', font=('', 10))
        #self.region_label.grid(row=0, column=0, pady=10)
        self.region_label.place(x=30,y=33)
        self.region_label.configure(background='white')
        
        self.district_label = ttk.Label(self.parent, text='Select District:', foreground='black', font=('', 10))
        #self.district_label.grid(row=1, column=0, pady=10)
        self.district_label.place(x=30, y=116)
        self.district_label.configure(background='white')
         
        self.select_region = ttk.Combobox(self.parent, values=['Avrupa','Asya','Trakya'], foreground='black', font=('', 10))
        self.select_region.set('Pick a Region')
        #self.select_region.grid(row=0, column=1, pady=10)
        self.select_region.place(x=140, y=30)
    
        self.select_region.bind("<<ComboboxSelected>>", self.filter_district)
        
        self.checkbox_var = tk.IntVar(value=1)
        self.checkbox = ttk.Checkbutton(self.parent, text='All Districts', variable=self.checkbox_var,
                                       command=self.checkbutton_callback)
        
        s = ttk.Style()
        s.configure('TCheckbutton', foreground='black',background='white')
        
        self.checkbox.place(x=140, y=115)
 
        self.load_img = Image.open('C:\\Users\\retter\\Desktop\\Tkinter\\import.png')

        
        self.load_img = self.load_img.resize((150, 40))#, Image.ANTIALIAS)
        self.load_img = ImageTk.PhotoImage(self.load_img)
        
        self.load_button = tk.Button(self.parent, command=self.load, text='Load Atoll DB',
                                     padx=10, pady=5) 
        
        self.load_button.place(x=28, y=235)

        #self.convert_button = ttk.Button(self.parent, text='Convert To KMZ', command=self.convert_kmz)
        
        self.convert_img = Image.open('C:\\Users\\retter\\Desktop\\Tkinter\\convert.png')
        
        self.convert_img = self.convert_img.resize((150, 40))#, Image.ANTIALIAS)
        self.convert_img = ImageTk.PhotoImage(self.convert_img)
        self.convert_button = tk.Button(self.parent, command=self.convert_kmz,
                                    text='Convert to KMZ', padx=10, pady=5) 
        #self.convert_button.grid(row=4, column=1)
        self.convert_button.place(x=180, y=235)
        
        self.listbox = tk.Listbox(self.parent, selectmode=tk.MULTIPLE, selectbackground="#f5424e")
        self.listbox.bind('<<ListboxSelect>>',self.listbox_selected)
     
        self.scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.listbox.yview)
       
        self.listbox.place(x=250, y=117)
           
        self.listbox.insert(tk.END, 'All Districts')
        self.listbox.config(height=0)
        # attach listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.configure(state=tk.DISABLED)
        self.scrollbar.config(command=self.listbox.yview)
 
    def checkbutton_callback(self):
        if(self.checkbox_var.get()==0):
            self.listbox.configure(state=tk.NORMAL)
            
            self.listbox.delete(0,tk.END)
        
            if(self.region=='Avrupa'):
                for i in self.avrupa_list:
                    self.listbox.insert(tk.END, i)
            elif(self.region=='Asya'):
                for i in self.asya_list:
                    self.listbox.insert(tk.END, i)
            elif(self.region=='Trakya'):
                for i in self.trakya_list:
                    self.listbox.insert(tk.END, i)
           
            
       
        if(self.checkbox_var.get()==1):
            self.listbox.configure(state=tk.DISABLED)
            
            self.avrupa_list = ['BEYLIKDUZU', 'BAKIRKOY', 'BESIKTAS', 'FATIH', 'EYUP', 'GAZIOSMANPASA', 'BEYOGLU',
                     'KAGITHANE', 'SARIYER', 'ZEYTINBURNU', 'SISLI', 'KUCUKCEKMECE',  'CATALCA',
                      'AVCILAR', 'SILIVRI','BAHCELIEVLER', 'ESENYURT', 'ARNAVUTKOY', 'BUYUKCEKMECE',
               'BAGCILAR', 'BASAKSEHIR', 'ESENLER', 'BAYRAMPASA', 'GUNGOREN','SULTANGAZI']
            self.asya_list = ['KADIKOY', 'USKUDAR', 'TUZLA', 'SANCAKTEPE', 'BEYKOZ', 'CEKMEKOY', 'PENDIK', 'KARTAL',
                     'MALTEPE', 'UMRANIYE','SILE', 'ATASEHIR', 'ADALAR', 'SULTANBEYLI']
            self.trakya_list = ['TEKIRDAG','EDIRNE','KIRKLARELI']
        

    def load(self):
        
        
        name = askopenfilename(filetypes=[('Excel', ('*.xls', '*.xslm', '*.xlsx'))])
        
        site_cols = ['Longitude', 'Latitude', 'SITE_NAME', 'SITE_NAME_3G', 'SITE_NAME_4G', 'CONSTRUCTION_TYPE',
                'CONSTRUCTION_HEIGHT','Equipment','DISTRICT','SITE_ADDRESS','Name','CITY']
    
        gsm_cols = ["Azimuth (°)",'OMC_CELLNAME','LAC', 'BCCH', 'DX (m)', 'DY (m)', 'Site', 'Antenna',
                'Mechanical Downtilt (°)','Height (m)','BSC']

        umts_cols = ["Azimuth (°)", 'Transmitter', 'DX (m)', 'DY (m)', 'Site', 'SECTOR_TYPE',
                  'Antenna', 'Mechanical Downtilt (°)','Height (m)']
    
        umts_cell_cols = ['Transmitter', 'LAC', 'URA', 'Primary scrambling code', 'OMC_CELLNAME',
                      'Max Power (dBm)', 'RNC', 'Pilot Power (dBm)']
        lte_cols = ['Site', 'Antenna', 'Height (m)', 'Transmitter', "Azimuth (°)", 'Mechanical Downtilt (°)',
            'DX (m)', 'DY (m)'  ]
    
        lte_cell_cols = ['Transmitter', 'TAC', 'Physical Cell ID', 'OMC_CELLNAME', 'Max Power (dBm)',
                 'RS EPRE per antenna port (dBm)' ] 

        if name:
            self.site_df = pd.read_excel(name, sheet_name='Site', usecols = site_cols)
            self.gsm_df = pd.read_excel(name, sheet_name='GSM', usecols = gsm_cols)
            self.umts_df = pd.read_excel(name, sheet_name='UMTS', usecols = umts_cols)
            self.umts_cell_df = pd.read_excel(name, sheet_name='UMTS_CELL', usecols=umts_cell_cols)
            self.lte_df = pd.read_excel(name, sheet_name='LTE', usecols=lte_cols)
            self.lte_cell_df = pd.read_excel(name, sheet_name='LTE_CELL', usecols = lte_cell_cols)

            self.filename = name
            
            '''
            
            self.site_df.to_pickle('site_df.pkl')
            self.gsm_df.to_pickle('gsm_df.pkl')
            self.umts_df.to_pickle('umts_df.pkl')
            self.umts_cell_df.to_pickle('umts_cell_df.pkl')
            self.lte_cell_df.to_pickle('lte_cell_df.pkl')
            self.lte_df.to_pickle('lte_df.pkl')
            '''
            print(self.site_df)
            
    def filter_district(self, event):
        
        self.region = self.select_region.get()
        #self.scrollbar.grid(row=1, column=3, sticky='nsw')
        self.scrollbar.place(x=370, y=116, height=103)
        #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(height=6)
        
        self.listbox.delete(0,tk.END)
        
        if(self.region=='Avrupa'):
            for i in self.avrupa_list:
                self.listbox.insert(tk.END, i)
        elif(self.region=='Asya'):
            for i in self.asya_list:
                self.listbox.insert(tk.END, i)
        elif(self.region=='Trakya'):
            for i in self.trakya_list:
                self.listbox.insert(tk.END, i)     
        
        self.checkbutton_callback()
        
    def listbox_selected(self, event):
              
        values = []
        values = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        
        
        values_str = ', '.join(values)
        
        if(self.region == 'Avrupa'):
            self.avrupa_list = values
        if(self.region == 'Asya'):
            self.asya_list = values
        if(self.region == 'Trakya'):
            self.trakya_list = values  

        #tk.Label(self.parent, text=values_str).grid(row=5, column=1)
        
        
    def convert_kmz(self):
        
        site_df = self.site_df 
        gsm_df = self.gsm_df
        umts_df = self.umts_df
        umts_cell_df = self.umts_cell_df
        lte_df = self.lte_df
        lte_cell_df = self.lte_cell_df
        
        '''
        
        site_df = pd.read_pickle('site_df.pkl')
        gsm_df = pd.read_pickle('gsm_df.pkl')
        umts_df = pd.read_pickle('umts_df.pkl')
        umts_cell_df = pd.read_pickle('umts_cell_df.pkl')
        lte_cell_df = pd.read_pickle('lte_cell_df.pkl')
        lte_df = pd.read_pickle('lte_df.pkl')
        '''
       

        avrupa_camera = [41.056352, 28.915095, 23378, 3.000000, 15.000000]
        asya_camera = [41.033368,  29.261240, 41670, -1.000000, 6.000000]
        trakya_camera = [41.362845, 26.938775, 260711, -3.000000, 6.000000]

        self.region = self.select_region.get()

        if(self.region == 'Avrupa'):
            camera = avrupa_camera
            site_sub = site_df[site_df['DISTRICT'].isin(self.avrupa_list)]
            print(site_sub)
            kml_path = "\\Users\\retter\\Desktop\\Tkinter\\AVRUPA.kmz"
            
        elif(self.region == 'Asya'):
            camera = asya_camera
            site_sub = site_df[site_df['DISTRICT'].isin(self.asya_list)]
            kml_path = "\\Users\\retter\\Desktop\\Tkinter\\ASYA.kmz"
        
        #else:
        elif(self.region == 'Trakya'):
            camera = trakya_camera
            site_sub = site_df[site_df['CITY'].isin(self.trakya_list)]
            kml_path = "\\Users\\retter\\Desktop\\Tkinter\\TRAKYA.kmz"
            
        
        
        #camera = asya_camera
        
        #camera = trakya_camera

        #site_sub = site_df[site_df['DISTRICT'].isin(asya_list)] # ASYA
         # AVRUPA
        #site_sub = site_df[site_df['CITY'].isin(trakya_list)] # TRAKYA

        #kml_path = "\\Users\\retter\\Desktop\\KML\\ASYA.kmz"
        
        #kml_path = "\\Users\\retter\\Desktop\\KML\\TRAKYA.kmz"

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

        if(self.region == 'Trakya'):
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
       
        else:
            
            for district in site_sub[site_sub['CITY']=='ISTANBUL']['DISTRICT'].unique():
    
                    district_dic[district] = site_folder.newfolder()
                    district_dic[district].name = district
    
                    district_dic_gsm[district] = gsm_folder.newfolder()
                    district_dic_gsm[district].name = district
                    district_dic_umts[district] = umts_folder.newfolder()
                    district_dic_umts[district].name = district
                    district_dic_lte[district] = lte_folder.newfolder()
                    district_dic_lte[district].name = district


        
 
        site_sub = site_sub.replace(np.nan, '', regex=True)
        gsm_df = gsm_df.replace(np.nan, '', regex=True)
        umts_df = umts_df.replace(np.nan, '', regex=True)
        umts_cell_df = umts_cell_df.replace(np.nan, '', regex=True)
        lte_df = lte_df.replace(np.nan, '', regex=True)
        lte_cell_df = lte_cell_df.replace(np.nan, '', regex=True)
        
        
        '''
        site_sub.fillna('', inplace=True)
        gsm_df.fillna('', inplace=True)
        umts_df.fillna('', inplace=True)
        umts_cell_df.fillna('', inplace=True)
        lte_df.fillna('', inplace=True)
        lte_cell_df.fillna('',inplace=True)
        '''

        #for i in range(1):
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

                umts_poly(coeff, cell_count, style_umts, float(lat_2), float(lon_2), int(row["Azimuth (°)"]),
                          district_dic_umts[district], region_umts, 
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

                lte_poly(coeff, cell_count, style_linestring, lte_band_check, band_dict[str(row['Transmitter'])[-2]],
                         float(lat_2), float(lon_2),
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


if __name__ == '__main__':
    #root = tk.Tk()
  
    root = ThemedTk()
    root.geometry('450x350')
    root.iconbitmap('C:\\Users\\retter\\Desktop\\Tkinter\\cropped_1.ico')
    root.title(' KMZ Maker')
    #p1 = tk.PhotoImage(file = 'C:\\Users\\retter\\Desktop\\Tkinter\\icon.png')
# Icon set for program window
    #root.iconphoto(False, p1)
    #root.set_theme_advanced(theme_name='arc',hue=1.59, saturation=2)
    root.option_add('*TCombobox*Listbox.selectBackground', '#f5424e')
    root.option_add("*TCombobox*Listbox*Font", ('',10))
    root.configure(background='white')
    top = MyWindow(root)
    root.mainloop()





