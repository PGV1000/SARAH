import os
from osgeo import gdal
import pathlib

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath

def Reproject(inputRasterPath):

    inputRaster = gdal.Open(inputRasterPath)
    outputRasterPath =  "./Reproject/Reproject" + pathlib.Path(inputRasterPath).suffix
    print(inputRaster.GetGeoTransform())
    print(inputRaster.GetProjection())


    gdal.Warp(outputRasterPath,inputRaster, dstSRS = 'EPSG:4326')
    inputRaster = None
