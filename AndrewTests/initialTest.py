import numpy as np
import matplotlib.pyplot as plt

# google earth engine import
import ee
ee.Authenticate()
ee.Initialize()
# this code is a quick test of GEE taken from https://developers.google.com/earth-engine/guides/python_install
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())