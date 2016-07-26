from EdgeManipulator import EdgeSharpener
import argparse
import time

#configure argument parser to read image
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file being processed")
ap.add_argument("-o", "--output", help = "filename to write sharpened image", default=time.strftime("%Y%m%d-%H%M%S")+".jpg")

#parse arguments
args = vars(ap.parse_args())
inputImage = args["image"]
outputFile = args["output"]

mEdgeSharpener = EdgeSharpener(inputImage)
mEdgeSharpener.sharpenImage(outputFile)