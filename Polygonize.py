import os
from osgeo import gdal, ogr, osr

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath

def Polygonize():
    output = gdal.Open('.\BinMask\BinMask.tif')
    outband = output.GetRasterBand(1)

    srs  = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    output_shape_path  = '.\Polygonize\Polygonized'

    output_layername = output_shape_path
    driver = ogr.GetDriverByName("ESRI Shapefile")
    output_ds = driver.CreateDataSource(output_layername + ".shp" )
    output_layer = output_ds.CreateLayer(output_layername, srs)

    gdal.Polygonize(outband,outband, output_layer, -1, [], callback=None )
    outband = None
    output = None
