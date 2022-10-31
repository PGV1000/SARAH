import os
from osgeo import gdal
import glob

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath

def Reproject(inputRasterPath):

    inputRaster = gdal.Open(inputRasterPath)
    outputRasterPath =  './Reproject/Reproject.tiff' #+ os.path.basename(glob.glob('./Input/*.tif*')[0])
    print(inputRaster.GetGeoTransform())
    print(inputRaster.GetProjection())


    gdal.Warp(outputRasterPath,inputRaster, dstSRS = 'EPSG:4326', format = 'GTiff', dstNodata = 0 ) #format = 'GTiff', dstNodata = 0
    inputRaster = None
