# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:53:07 2022
@author: s1834371
"""
import os
import xarray as xr
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import ee
import geemap

def flatten(lst):
    for i in lst:
        if isinstance(i, list):
            for v in flatten(i):
                yield v
        else:
            yield i

# =============================================================================
# Collect sentinel tiles and filter to Greenland region of interest
# =============================================================================
ee.Initialize()

ROI_dir = 'C:/Users/s1834371/Documents/PhD/GFSTS/Code/GIS/ROI/ROI.geojson'
ROI = geemap.geojson_to_ee(ROI_dir)

#Filtering sentinel-2 TOA to cloud percentage, rough greenland ROI and timeframe
s2_dataset = ee.ImageCollection('COPERNICUS/S2_HARMONIZED')\
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))\
                .filter(ee.Filter.bounds(ROI))\
                .filterDate('2015-06-01', '2022-10-01')

# Loop through each file, open file, retrieve date and latlon, compare
parent_data_dir = 'C:/Users/s1834371/Documents/PhD/GFSTS/Data/OMG/AXCTD' #file directory of in-situ data

# Count number of files to list through
file_list = []
for (dir_path, dir_names, file_names) in os.walk(os.path.normpath(parent_data_dir)):
    file_list.extend(file_names)
    
len_files = len(file_list) #length of list of all files
count = 1 #for loop code
tile_count = 0 #number of matching tiles
dict_count = 0
master_dict = {} #master dictionary to save band values and temp, salinity, etc to.
            
for path, subdirs, files in os.walk(os.path.normpath(parent_data_dir)):
    for name in files:
        print(count, '/', len_files)
        file_dir = os.path.join(path, name)
        
        #-------open netcdf insitu datafile--------------------
        CTD_data = xr.open_dataset(file_dir, engine='netcdf4')
        #print(CTD_data.variables)
        
        #--------subsetting information------------------------
        lon = float(CTD_data.lon.values[0])
        lat = float(CTD_data.lat.values[0])
        time = CTD_data.time.isel(profile=0).values
        water_depth = float(CTD_data.depth[0].values[0])
        temperature = float(CTD_data.temperature[0].values[0])
        salinity = float(CTD_data.salinity[0].values[0])
        
        if isinstance(time, np.ndarray): #checking if time is np.ndarray or np.datetime64
            time = next(t for t in time if t == t) # Returns first non=NaN elemnt
        else:
            time = time   
        time = pd.to_datetime(time)
        
        #---------filter sentinel tiles-----------------------------------
        start_time = (time - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        end_time = (time + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        obs_point = ee.Geometry.Point([lon, lat])
        
        s2_dataset_filtered = s2_dataset.filter(ee.Filter.bounds(obs_point)).filterDate(start_time, end_time)
        count_tiles = s2_dataset_filtered.size()
        count_tiles = count_tiles.getInfo()
        print('Matching tiles:', str(count_tiles))
        
        if count_tiles >= 1:
            dict_count = dict_count + 1
            buffer_area = obs_point
            buffer_area = buffer_area.buffer(100) # create a 100m circular buffer around the observation point
            clipped_tile = s2_dataset_filtered.first().clip(buffer_area)
            reduced_tile = clipped_tile.reduceRegion(ee.Reducer.mean(), buffer_area)
           
            band_dict = reduced_tile.getInfo()   
            band_dict['no_tiles'] = count_tiles
            band_dict['temperature'] = temperature
            band_dict['salinity'] = salinity
            band_dict['depth'] = water_depth
            band_dict['lon'] = lon
            band_dict['lat'] = lat
            band_dict['start_date'] = start_time
            band_dict['end_date'] = end_time
            
            if dict_count==1:
               master_dict = band_dict
            else:
                dd = defaultdict(list)
                for d in (master_dict, band_dict): # you can list as many input dicts as you want here
                     for key, value in d.items():
                         dd[key].append(value)
                master_dict = dd
            #print(master_dict)
        print(lon, lat, start_time, end_time)
        count = count + 1
        tile_count = tile_count + count_tiles
        print(tile_count)
        print('------------------\n')
print('\n-------------------------------')
print('Total matching tiles:', tile_count)
dd = defaultdict(list)
for key, value in master_dict.items():
         value = list(flatten(value))
         dd[key] = value
master_dict = dd
print(master_dict)
        
print('\nSaving to CSV file...')
output_df = pd.DataFrame.from_dict(master_dict)
output_df.to_csv('output_dataframe_AXCTD.csv')
        
        