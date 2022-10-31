import os
import glob
import rasterio
import rasterio.mask
import NoDataZero
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
def BinMask(inputRasterPath):
    print('------------Binmask------------')
    print('Creating BinMask...')
    print('Getting the image file...')
    print(inputRasterPath)
    print('Creating the output file name...')
    outputRasterPath = '.\BinMask\BinMask.tiff'
    print(outputRasterPath)

    originalRaster = rasterio.open(glob.glob('./Input/*.tif*')[0])
    originalRasterArray = originalRaster.read()

    if originalRaster.dtypes[0]== 'uint16' and 65535 in originalRasterArray:
        NoDataZero.NoDataZero(inputRasterPath)
    originalRaster.close()
    originalRasterArray = None

    src = rasterio.open(inputRasterPath)
    rasterArray = src.read()
    
    img = gdal.Open(inputRasterPath, 1) #1 means editing mode
    if src.dtypes[0]== 'uint16' or src.dtypes[0]=='uint8':
        print('Setting nodata to 0...')
        nodata = 0
        # # proj = img.GetProjection()
        # gt = img.GetGeoTransform()
        for i in range(1, img.RasterCount + 1):
        # #     # set the nodata value of the band
            img.GetRasterBand(i).SetNoDataValue(0)
        # # unlink the file object and save the results
    elif src.dtypes[0]=='float32':
        print('Setting nodata to -9999...')
        nodata = -9999
        # # proj = img.GetProjection()
        # gt = img.GetGeoTransform()
        for i in range(1, img.RasterCount + 1):
        # #     # set the nodata value of the band
            img.GetRasterBand(i).SetNoDataValue(-9999)
        # # unlink the file object and save the results
    img = None


    
    

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

    profile = src.profile
    profile.update({'nodata': nodata})

    with rasterio.open(outputRasterPath,'w+',**profile) as dst: 
        dst.write(sieved_msk,1) # (np.array, number of bands?)
    sieved_msk = None
    msk = None
    src = None
    rasterArray = None 

    