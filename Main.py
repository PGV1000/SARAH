import sys
import os
import pathlib
import glob
import Reproject
import Binmask
import Polygonize
import Buffer
import Clip

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit


# Gather our code in a main() function
def main():
    # print ('Hello there', sys.argv[1])
    input_raster_path = glob.glob('./Input/*.tif*')[0]
    outputRasterPath = './Output/'+os.path.basename(input_raster_path)
    print(input_raster_path)
    bufferMaskPath = '.\Buffer\Buffer.shp'
    seaMaskPath = '.\Mask\Mask.shp'
    Reproject.Reproject(input_raster_path)
    reprojectedRasterPath = "./Reproject/Reproject" + pathlib.Path(input_raster_path).suffix

    Binmask.BinMask(reprojectedRasterPath)
    Polygonize.Polygonize()
    while True:
        try:
            isBuffer = input("Do you want to buffer the image? y/n : ") 
            if isBuffer=='y' or isBuffer=='Y':
                Buffer.Buffer(reprojectedRasterPath)
                Clip.Clip(reprojectedRasterPath, bufferMaskPath, outputRasterPath)
                break
            elif isBuffer=='n'or isBuffer=='N':
                print('Skipping buffering process...')
                break
            else:
                print("The input is not correct")   
        except ValueError:
            print("Invalid")
            continue
    Clip.Clip(reprojectedRasterPath,seaMaskPath,outputRasterPath)

if __name__ == '__main__':
  main()