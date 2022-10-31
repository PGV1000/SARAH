import os
import rasterio
import rasterio.mask
from rasterio.features import sieve
from affine import Affine

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath



def ChangeGeoTransform(inputRasterPath,falseLat,falseLon):

    print('-----------ChangeGeoTransorm-----------')
    outputRasterPath = inputRasterPath

    print('Getting the image file...')
    with rasterio.open(inputRasterPath) as src:
        rasterArray = src.read()
        new_transform = src.transform
        new_profile = src.profile

    
    print('Input geotransorm: \n',src.transform)

    if new_transform[2] > 130:
        realLat = 51.3080096
        realLon = 144.315944
    else: 
        realLat = 73.8726666667
        realLon = 46.5333333333

    print('Calculating coordinate difference...')
    deltaLat = realLat - falseLat
    deltaLon = realLon - falseLon

    print('Coordinate difference: \n',deltaLat,deltaLon)

    print('Applying new geotransform....')
    
    translated = new_transform.translation(new_transform[2]+deltaLon,new_transform[5]+deltaLat)
    
    new_profile.update(transform =Affine(src.transform[0],src.transform[1],translated[2],src.transform[3],src.transform[4],translated[5]))

    print('Saving the output...')
    with rasterio.open(outputRasterPath,'w',**new_profile) as dst: 
        dst.write(rasterArray) # (np.array, number of bands?)
    rasterArray = None

    with rasterio.open(outputRasterPath) as output:
        print('Output geotransorm: \n',output.transform)

    output = None

