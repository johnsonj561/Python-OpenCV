from ComponentTracker import ComponentTracker
import argparse

#configure argument parser to read image
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file being processed")
ap.add_argument("-lt", "--low", help = "low threshold value used for creating binary image", type=int, default=0)
ap.add_argument("-ht", "--high", help = "high threshold value used for creating binary image", type=int, default=40)
ap.add_argument("-ma", "--minarea", help = "minimum pixel area to detect during contour detection, smaller objects contours will be ignored", type=int, default=250)

#parse arguments
args = vars(ap.parse_args())
inputImage = args["image"]
lowThreshold = args["low"]
highThreshold = args["high"]
minComponentArea = args["minarea"]

#instantiate ComponentTracker object with input image
mComponentTracker = ComponentTracker(inputImage)
#threshold image to create binary image
mComponentTracker.thresholdImage(lowThreshold, highThreshold)
#detect contour rectangle that is >= minCompnentArea, neglecting insignificantly small contours
rectangle = mComponentTracker.findContourRectangle(minComponentArea)

#if component was found, draw contours and commponent details on image & display
if rectangle:
  mComponentTracker.drawContoursFromRectangle(rectangle)
  mComponentTracker.drawRectangleDetails(rectangle)
  mComponentTracker.displayOutput()
  
else:
  print("No Components Found")

