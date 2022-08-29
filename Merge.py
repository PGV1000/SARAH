from types import CoroutineType
from osgeo import gdal
import numpy as np
import glob


imageName = glob.glob('*.tif')[0] # Grab a tif file name 
image = gdal.Open(imageName) # Open this tif with gdal and put it in "image" variable
maskedImage = gdal.Warp("Masked.tif", image, cutlineDSName = 'Mask.shp', cropToCutline = True, dstNodata = np.nan)
image = maskedImage = None
