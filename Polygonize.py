import os
os.environ['PROJ_LIB'] = 'C:\OSGeo4W\share\proj'
os.environ['GDAL_DATA'] = 'C:\OSGeo4W\apps\gdal\share\gdal'
from osgeo import gdal, ogr, osr

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
