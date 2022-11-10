import ee 
import geemap

ee.Initialize()
ROI = geemap.geojson_to_ee(r'C:/Users/s1834371/Documents/PhD/SENSE_training/Bogs/ROI/BogsOnFire_ROI.geojson')