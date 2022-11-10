import numpy as np
import matplotlib.pyplot as plt
import cartopy as ctpy
import cartopy.crs as ccrs

# google earth engine import
import ee
import geemap
#ee.Authenticate()
ee.Initialize()
# this code is a quick test of GEE taken from https://developers.google.com/earth-engine/guides/python_install
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
