import os
import rasterio
import numpy as np
from osgeo import gdal

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath


def NoDataZero(inputRasterPath):
  print('------------NoDataZero------------')
  # Getting original image path
  print('Getting the image file...')
  print(inputRasterPath)
  # Setting output path
  print('Creating the output file name...')
  outputRasterPath = inputRasterPath
  print(outputRasterPath)

  src = rasterio.open(inputRasterPath,'r+')
  srcArray = src.read()

  img = gdal.Open(inputRasterPath,1) # 1 means editing mode
  if src.dtypes[0]== 'uint16' or src.dtypes[0]=='uint8':
    nodata = 0
  # # proj = img.GetProjection()
  # gt = img.GetGeoTransform()
    for i in range(1, img.RasterCount + 1):
  # # # set the nodata value of the band
      img.GetRasterBand(1).SetNoDataValue(nodata)
  elif src.dtypes[0]=='float32':
    nodata = -9999
  # # proj = img.GetProjection()
  # gt = img.GetGeoTransform()
    for i in range(1, img.RasterCount + 1):
  # # # set the nodata value of the band
      img.GetRasterBand(1).SetNoDataValue(nodata)
  img = None


  print('Peek: ', srcArray)
  print('Size: ',src.shape)
  print('Bands count: ',src.count)
  print('CRS: ', src.crs)
  print('Transforms: ', src.transform)
  print('Bounds: ', src.bounds)
  print('Formats: ',src.dtypes)
  print('Nodata values: ',src.nodatavals)
  print(src.nodata)

  print('Converting 65535 to 0...')
  binmask = np.where((srcArray != 65535),srcArray,nodata)
  

  print('Creating the output profile...')
  profile = src.profile
  profile.update({"nodata" : 0,})
  src.close()
  srcArray = None
  

  print('Saving the output...')
  with rasterio.open(outputRasterPath,'w+',**profile) as dst:
    dst.write(binmask)
  print('Done')