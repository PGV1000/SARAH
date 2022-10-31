import sys
import os
from pathlib import Path
from configparser import ConfigParser
import shutil
import rasterio
import glob
import Reproject
import Binmask
import Polygonize
import Buffer
import Clip
import ChangeGeotransform


config = ConfigParser()
config.read('config.ini')
projLibPath = config['PATHS']['proj_lib']
gdalDataPath = config['PATHS']['gdal_data']
os.environ['PROJ_LIB'] = projLibPath
os.environ['GDAL_DATA'] = gdalDataPath


def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit


# # Gather our code in a main() function
def main():

    while True:
        try:
            isBuffer = input("Do you want to buffer the image? y/n : ")
            if isBuffer == 'y' or isBuffer == 'Y':
                bufferDistance = float(input("Enter buffer distance (Press 'Enter' to apply default value: -0.01): ") or '-0.01') 
                break
            elif isBuffer=='n'or isBuffer=='N':
                print('Skipping the buffering process...')
                break
            else:
                print("The input is not correct")   
        except ValueError:
            print("Invalid")
            break
    
    while True:
        try:
            isChangeGT = input("Do you want to change the geotransorm of the image? y/n : ")
            if isChangeGT == 'y' or isChangeGT == 'Y':
                while True:
                    try:
                        falseLat = float(input("Enter the visible Latitude of an object: "))
                    except ValueError:
                            print("Error! Latitude value must be float. Example: 50.34512332")
                    else:
                            break

                while True:
                    try:
                        falseLon = float(input("Enter the visible Longitude of an object: "))
                    except ValueError:
                        print("Error! Longitude value must be float. Example: 50.34512332")
                    else:
                        break
                break
            elif isChangeGT=='n'or isChangeGT=='N':
                print('Skipping the changing geotrasform process...')
                break
            else:
                print("The input is not correct")
        except ValueError:
            print("Invalid")
            break

    
    
    inputRasterPath = glob.glob('./Input/*.tif*')[0]
    print(inputRasterPath)

    outputFolder = './Output/'+ Path(inputRasterPath).stem + '/'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    outputRasterPath = outputFolder + Path(inputRasterPath).stem+'.tiff'
    # outputRasterPath = './Output/'+os.path.basename(inputRasterPath)

    with rasterio.open(inputRasterPath) as src:
        inputTransform = src.transform

    if inputTransform[2] > 130:
        seaMaskPath = '.\Mask\Sakhalin\Mask.shp'
    else: 
        seaMaskPath = '.\Mask\BarentSea\Mask.shp'



    bufferMaskPath = '.\Buffer\Buffer.shp'
    

    Reproject.Reproject(inputRasterPath)

    reprojectedRasterPath = glob.glob('./Reproject/Reproject.tiff')[0]

    if isChangeGT == 'y' or isChangeGT == 'Y':
        ChangeGeotransform.ChangeGeoTransform(reprojectedRasterPath,falseLat,falseLon)
        
    shutil.copyfile(reprojectedRasterPath, outputRasterPath)

    with rasterio.open(reprojectedRasterPath) as src:
        inputTransform = src.transform

    if inputTransform[2] > 130:
        seaMaskPath = '.\Mask\Sakhalin\Mask.shp'
    else: 
        seaMaskPath = '.\Mask\BarentSea\Mask.shp'

    
            

    
    
    Binmask.BinMask(reprojectedRasterPath)
    Polygonize.Polygonize()
    
    while True:
        try:
            if isBuffer=='y' or isBuffer=='Y':
                Buffer.Buffer(reprojectedRasterPath,bufferDistance)
                Clip.Clip(reprojectedRasterPath, bufferMaskPath)
                break
            elif isBuffer=='n'or isBuffer=='N':
                print('Skipping buffering process...')
                break  
        except ValueError:
            print("Invalid")
            break
    Clip.Clip(reprojectedRasterPath,seaMaskPath)

    clippedRasterPath = glob.glob('./Clip/*.tif*')[0]
    outputRasterPath = outputFolder + 'CL_'+os.path.basename(inputRasterPath)
    shutil.copyfile(clippedRasterPath, outputRasterPath)


if __name__ == '__main__':
  main()