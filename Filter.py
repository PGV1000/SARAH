import os
os.environ['PROJ_LIB'] = 'C:\OSGeo4W\share\proj'
os.environ['GDAL_DATA'] = 'C:\OSGeo4W\apps\gdal\share\gdal'
import glob
from osgeo import gdal
import cv2


print('Getting the image file...')
dataset = glob.glob('.\Filter\*.tif')
print(dataset)
print('Creating the output file name...')
output_raster_path = '.\Filter\Filtered_' + os.path.basename(dataset[0])

#Getting projection and geotransoforms
img = gdal.Open(dataset[0])
proj = img.GetProjection() 
print('Projection: ', proj)
gt = img.GetGeoTransform() 
print('GeoTransform: ', gt)
img = None



# #############
# Gaussian blur
print('Reading the image...')
img = cv2.imread(dataset[0])
print('Applying Gaussian filter...')
gaussFiltered = cv2.GaussianBlur(img,(3,3),0,borderType = cv2.BORDER_CONSTANT)
print('Saving the filtered image...')
cv2.imwrite(output_raster_path,gaussFiltered)
cv2.waitKey(0)
print('Done...')
# #############


print('Applying projection...')

print('Getting the filtered image...')
dataset = glob.glob('.\Filter\Filtered_*.tif')
print(dataset)

img = gdal.Open(dataset[0])
print('Setting projection...')
img.SetProjection(proj)
print('Setting geotransforms...')
img.SetGeoTransform(gt)
img = None



# #############