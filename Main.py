# import modules used here -- sys is a very standard one
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)

import sys
sys.excepthook = show_exception_and_exit
import Binmask
import Polygonize
import Buffer
import Clip




# Gather our code in a main() function
def main():
    # print ('Hello there', sys.argv[1])
    bufferMaskPath = '.\Buffer\Buffer.shp'
    seaMaskPath = '.\Mask\Mask.shp'
    Binmask.BinMask()
    Polygonize.Polygonize()
    while True:
        try:
            isBuffer = input("Do you want to buffer the image? y/n : ") 
            if isBuffer=='y' or isBuffer=='Y':
                Buffer.Buffer()
                Clip.Clip(bufferMaskPath)
                break
            elif isBuffer=='n'or isBuffer=='N':
                print('Skipping buffering process...')
            else:
                print("The input is not correct")      
        except ValueError:
            print("Invalid")
            continue
    Clip.Clip(seaMaskPath)



  # Command line args are in sys.argv[1], sys.argv[2] ..
  # sys.argv[0] is the script name itself and can be ignored

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()