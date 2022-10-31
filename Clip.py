
import pathlib
import glob
import os
import fiona
import rasterio
import rasterio.mask
import numpy as np

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath

def Clip(inputRasterPath,maskPath):
    print('------------Clip------------')
    print('Starting clipping...')  

    print('Getting the mask file...')
    shpPath = maskPath
    if shpPath =='.\Buffer\Buffer.shp':
        print('Creating the output file name...')
        outputRasterPath = inputRasterPath
    else:
        print('Creating the output file name...')
        outputRasterPath = './Clip/Clip.tiff' #+ os.path.basename(glob.glob('./Input/*.tif*')[0]) #'./Clip/Clip'+  pathlib.Path(inputRasterPath).suffix

    print('Opening the mask file... ')
    with fiona.open(shpPath, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
    print(shpPath)
        
    print('Opening the image file...')
    with rasterio.open(inputRasterPath) as src:
        print('Clipping the image...')
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    print('Configuring the output file metadata...')
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform,
                    })

    print('Saving the output file...')
    with rasterio.open(outputRasterPath, "w", **out_meta) as dest:
        dest.write(out_image)
        
    print('Done')