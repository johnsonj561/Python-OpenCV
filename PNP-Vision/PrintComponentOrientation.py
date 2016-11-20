from ComponentTracker import ComponentTracker
import argparse
import cv2
import time

def main():
  # Configure argument parser to read image
  ap = argparse.ArgumentParser()
  ap.add_argument("-i", "--image", help = "path to the image file being processed", default =0)
  ap.add_argument("-lt", "--low", help = "low threshold value used for creating binary image", type=int, default=0)
  ap.add_argument("-ht", "--high", help = "high threshold value used for creating binary image", type=int, default=40)
  ap.add_argument("-ma", "--minarea", help = "minimum pixel area of contour; small contours will be ignored", type=int, default=250)
  # Parse arguments
  args = vars(ap.parse_args())
  imagePath = args["image"]
  lowThreshold = args["low"]
  highThreshold = args["high"]
  minComponentArea = args["minarea"]

  # If no input image path was provided, then capture image on USB camera, save image, and assign imagPath
  if imagePath == 0:
    imagePath = captureImage()
    
  # Create ComponentTracker object using image path
  mComponentTracker = ComponentTracker(imagePath)
  
  # Sharpen image to improve results of contour detection
  # OPTIONAL
  # mComponentTracker.sharpenImage()
  
  # Threshold image and create binary image
  mComponentTracker.thresholdImage(lowThreshold, highThreshold)
  
  # Detect contour rectangle that is >= minCompnentArea, neglecting insignificantly small contours
  rectangle = mComponentTracker.findContourRectangle(minComponentArea)

  # Return results to user
  if rectangle:
    mComponentTracker.drawContoursFromRectangle(rectangle)
    mComponentTracker.drawRectangleDetails(rectangle)
    print(mComponentTracker.getRectangleDetails(rectangle))
  else:
    # We could try to sharpen image a 2nd time and check for a component
    # During testing, re-sharpening image has proven effective
    print("Null")

    
# Capture image from USB Camera and display to user
def captureImage():
    cam = cv2.VideoCapture(0)
    s, img = cam.read() 
    cv2.imshow("Test Picture", img)
    filename = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    cv2.imwrite(filename,img) 
    return filename
    

# Main
if __name__ == "__main__":
  main()