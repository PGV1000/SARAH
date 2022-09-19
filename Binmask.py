import os
import rasterio
import rasterio.mask
from osgeo import gdal
from rasterio.features import sieve

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath


# import numpy as np
def BinMask(input_raster_path):
    print('Creating BinMask...')

    print('Getting the image file...')
    print(input_raster_path)
    print('Creating the output file name...')
    output_raster_path = '.\BinMask\BinMask.tif'
    print(output_raster_path)

    img = gdal.Open(input_raster_path)
    nodata = 0
    # # proj = img.GetProjection()
    # gt = img.GetGeoTransform()
    for i in range(1, img.RasterCount + 1):
    # #     # set the nodata value of the band
        img.GetRasterBand(1).SetNoDataValue(nodata)
    # # unlink the file object and save the results
    img = None


    src = rasterio.open(input_raster_path)
    rasterArray = src.read()

    print('Peek: ', rasterArray)
    print('Size: ',src.shape)
    print('Bands count: ',src.count)
    print('CRS: ', src.crs)
    print('Transforms: ', src.transform)
    print('Bounds: ', src.bounds)
    print('Formats: ',src.dtypes)
    print('Nodata values: ',src.nodatavals)
    print(src.nodata)

    msk = src.read_masks(1)
    print('Mask shape: ', msk.shape)
    print('Mask peek: ',msk)

    sieved_msk = sieve(msk, size=800)
    print('Sieved Mask peek: ',sieved_msk)

    profile = {
    'driver': 'GTiff', 
    'dtype': src.dtypes[0], # np.uint8, np.uint16 etc.
    'nodata': 0, 
    'width': src.shape[1], 
    'height': src.shape[0],
    'count': 1, # bands count
    'crs': src.crs, 
    'transform': src.transform, 
    'tiled': False,
    'compress': None,
    }

    with rasterio.open(output_raster_path,'w',**profile) as dst: 
        dst.write(sieved_msk,1) # (np.array, number of bands?)
    sieved_msk = None
    msk = None
    src = None

    