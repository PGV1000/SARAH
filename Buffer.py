import sys
import os
import glob
from osgeo import ogr, osr

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath


def Buffer(input_raster_path, bufferDistance):
    print('Starting buffering...')

    print('Getting the shape file...')
    src_shape_path = glob.glob('.\Polygonize\Polygonized.shp')[0]
    print(src_shape_path)
    print('Creating the output file name...')
    output_shape_path = '.\Buffer\Buffer.shp'
    print(output_shape_path)


    # open .shp and get the layer
    inputShape = ogr.Open(src_shape_path)
    if inputShape is None:
        print ('Could not open shape file.')
        sys.exit(1)
    inputLayer = inputShape.GetLayer()

    print ("Number of layers", inputShape.GetLayerCount())
    # обращаемся к слою по индексу
    layer = inputShape.GetLayer( 0 )

    print ("Feature count", layer.GetFeatureCount())
    print ("Layer SRC", layer.GetSpatialRef())
    print ("Layer extent", layer.GetExtent())

    feat = layer.GetNextFeature()
    featDef = layer.GetLayerDefn() # схема (таблица атрибутов) слоя
    fieldDef = featDef.GetFieldDefn(0) # получаем i-тое поле
    print ("Field name", fieldDef.GetNameRef()) # и выводим информацию
    print ("Field type", fieldDef.GetType())
    print ("Field value", feat.GetFieldAsString(0))
    #   feat = layer.GetNextFeature() # переходим к следующему объекту

    geom = feat.GetGeometryRef()
    if geom is None:
        print ("Invalid geometry")

    bufferedGeom = geom.Buffer(bufferDistance,1)


    srs  = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    driverName = "ESRI Shapefile"
    drv = ogr.GetDriverByName( driverName )
    if drv is None:
        print ("%s driver not available.\n" % driverName)

    output_ds = drv.CreateDataSource(output_shape_path)
    if output_ds is None:
        print ("Creation of output file failed.\n")
        sys.exit( 1 )
    layer = output_ds.CreateLayer( "BUffered", srs, ogr.wkbPolygon)
    if layer is None:
        print ("Layer creation failed.")
        sys.exit( 1 )

    fieldDef = ogr.FieldDefn( "FileName", ogr.OFTString ) # имя поля и его тип
    fieldDef.SetWidth( 32 ) # длина поля
    
    if layer.CreateField ( fieldDef ) != 0:
        print ("Creating field failed.\n")
        sys.exit( 1 )
    
    # для чисел с плавающей точкой можно задать не только длину,
    # но и точность
    fieldDef = ogr.FieldDefn( "Area", ogr.OFTReal ) # имя поля и его тип
    fieldDef.SetWidth( 18 ) # длина поля
    fieldDef.SetPrecision( 6 ) # точность
    
    if layer.CreateField ( fieldDef ) != 0:
        print ("Creating field failed.\n")
        sys.exit( 1 )

    name = input_raster_path # значение атрибута
    feat = ogr.Feature( layer.GetLayerDefn() ) # создаем OGRFeature
    feat.SetField( "FileName", name ) # устанавливаем атрибут
    
    feat.SetGeometry(bufferedGeom) 

    if layer.CreateFeature( feat ) != 0:
        print ("Failed to create feature in shapefile.\n")
        sys.exit( 1 )
    
    # освобождаем память
    feat.Destroy()
    output_ds.Destroy()
