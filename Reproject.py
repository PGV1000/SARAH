from osgeo import gdal
import pathlib

def Reproject(inputRasterPath):

    inputRaster = gdal.Open(inputRasterPath)
    outputRasterPath =  "./Reproject/Reproject" + pathlib.Path(inputRasterPath).suffix
    print(inputRaster.GetGeoTransform())
    print(inputRaster.GetProjection())


    gdal.Warp(outputRasterPath,inputRaster, dstSRS = 'EPSG:4326')
    inputRaster = None
