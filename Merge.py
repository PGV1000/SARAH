# Gdal Algorithm - has a problem with output size and clipping it to input extent
# from types import CoroutineType
# from osgeo import gdal
# import numpy as np
# import glob

# # Grab a tif file name 
# imageName = glob.glob('*.tif')[0]

# # Open this tif with gdal and put it in "image" variable
# image = gdal.Open(imageName)

# # Clip an image with "Mask.shp" and return "Masked.tif"
# maskedImage = gdal.Warp("Masked.tif", image, cutlineDSName = 'Mask.shp', cropToCutline = True, dstNodata = np.nan)
# image = maskedImage = None

import fiona
import rasterio
import rasterio.mask
import glob


src_raster_path = glob.glob('*.tif')[0]

shp_file_path = "Mask.shp"

output_raster_path = src_raster_path[:-3] + '_masked.tif'

with fiona.open(shp_file_path, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

with rasterio.open(src_raster_path) as src:

    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})


with rasterio.open(output_raster_path, "w", **out_meta) as dest:
    dest.write(out_image)