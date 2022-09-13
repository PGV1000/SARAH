import os
os.environ['PROJ_LIB'] = 'C:\OSGeo4W\share\proj'
os.environ['GDAL_DATA'] = 'C:\OSGeo4W\apps\gdal\share\gdal'
import fiona
import rasterio
import rasterio.mask

def Clip(input_raster_path,maskPath,outputRasterPath):
    print('Starting clipping...')

    print('Getting the image file...')
    

    print('Getting the mask file...')
    shp_file_path = maskPath
    if shp_file_path =='.\Buffer\Buffer.shp':
        print('Creating the output file name...')
        outputRasterPath = input_raster_path
    else:
        print('Creating the output file name...')
        

    print('Opening the mask file... ')
    with fiona.open(shp_file_path, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        
    print('Opening the image file...')
    with rasterio.open(input_raster_path) as src:
        print('Clipping the image...')
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    print('Configuring the output file metadata...')
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    print('Saving the output file...')
    with rasterio.open(outputRasterPath, "w", **out_meta) as dest:
        dest.write(out_image)
        
    print('Done')