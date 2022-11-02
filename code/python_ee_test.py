# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:30:05 2022

@author: s1834371
"""

import os
import pandas as pd
import numpy as np

import ee
import geemap


# =============================================================================
# Collect sentinel tiles and filter to Greenland region of interest
# =============================================================================
ee.Initialize()

data_dir = 'C:/Users/s1834371/Documents/PhD/SENSE_training/Bogs' # direct of github repo

ROI_dir = data_dir + '/ROI/BogsOnFire_ROI.geojson' # ROI of wildfire region
ROI = geemap.geojson_to_ee(ROI_dir)

#Filtering sentinel-2 TOA to cloud percentage, rough greenland ROI and timeframe
s2_dataset = ee.ImageCollection('COPERNICUS/S2_HARMONIZED')\
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))\
                .filter(ee.Filter.bounds(ROI))\
                .filterDate('2019-04-01', '2022-10-01') # Filtering to study time period
            
