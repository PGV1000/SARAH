import os
from pathlib import Path
os.environ['PROJ_LIB'] = 'C:\OSGeo4W\share\proj'
os.environ['GDAL_DATA'] = 'C:\OSGeo4W\apps\gdal\share\gdal'
import rasterio
import rasterio.mask
import glob
from osgeo import gdal, ogr, osr
from rasterio.features import sieve
from rasterio.crs import CRS
# import numpy as np
print('Starting polygonizing...')

print('Getting the image file...')
src_raster_path = glob.glob('.\Polygonize\*.tif')[0]
print(src_raster_path)
print('Creating the output file name...')
output_raster_path = 'Mask_' + os.path.basename(src_raster_path)
print(output_raster_path)

img = gdal.Open(src_raster_path)
nodata = 0
# # proj = img.GetProjection()
# gt = img.GetGeoTransform()
for i in range(1, img.RasterCount + 1):
# #     # set the nodata value of the band
    img.GetRasterBand(1).SetNoDataValue(nodata)
# # unlin(k the file object and save the results
img = None


src = rasterio.open(src_raster_path)
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
# plt.imshow(msk)

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

# arrayFilled = rasterArray.fill(0)
with rasterio.open('Polygonize\Mask.tif','w',**profile) as dst: 
    dst.write(sieved_msk,1) # (np.array, number of bands?)

output = gdal.Open('Polygonize\Mask.tif')
outband = output.GetRasterBand(1)

srs  = osr.SpatialReference()
srs.ImportFromEPSG(4326)

output_shape_path = output_raster_path = './Polygonize/Polygonized_' + Path(os.path.basename(src_raster_path)).stem

output_layername = output_shape_path
driver = ogr.GetDriverByName("ESRI Shapefile")
output_ds = driver.CreateDataSource(output_layername + ".shp" )
output_layer = output_ds.CreateLayer(output_layername, srs)

gdal.Polygonize(outband,outband, output_layer, -1, [], callback=None )
outband = None
output = None
