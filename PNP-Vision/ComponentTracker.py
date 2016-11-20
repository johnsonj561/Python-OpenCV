# PNP Computer Vision System for identifying ICs and analyzing IC orientation
# Justin Johnson
# FAU, Fall 2016
import numpy as np
import cv2
import time

# ComponentTracker class accepts input image path and provides functionality:
# Preprocessing, identify countours, drawing best fit rectangle and return orientation attributes
class ComponentTracker():
  # Read input image path to be processed
  def __init__(self, input_image):
    self.input_image = cv2.imread(input_image)
  
  # Threshold image and generate binary output image
  # @param int l = lower bound of threshold
  # @param int h = upper bound of threshold
  # @param boolean showImage displays image if true, default false
  def thresholdImage(self, l, h, showImage = False):
    # Set lower and upper bounds for image thresholding
    # 3 element array handles 3 channels, R G B
    # Another option: convert img to gray scale and threshold on 1 channel
    lower = np.array([l, l, l])
    upper = np.array([h, h, h])
    # inRange returns binary value 1/0:
    # Returns 1 if lower <= input <= upper, else returns 0
    self.binary_image = cv2.inRange(self.input_image, lower, upper)
    # If @param showImage = true, display image to user
    if showImage:
      cv2.imshow("Thresholded Output", self.binary_image)
    
    
  # Sharpen image by filtering image with a 5x5 edge enhancing kernal
  # Linear Filter is applied to original image found at 'input_image' path
  # 1. Kernal anchor (center) is placed above determined pixel
  # 2. Multiply kernal coefficients by corresponding image pixel values
  # 3. Sum all results and place result in position of input's anchor value
  # 4. Repeat process for all pixels in image
  def sharpenImage(self):
    kernel_sharpen = np.array([[-1, -1, -1, -1, -1],
                               [-1, 2, 2, 2, -1],
                               [-1, 2, 8, 2, -1],
                               [-1, 2, 2, 2, -1],
                               [-1, -1, -1, -1, -1]]) / 8.0
    # filter2D applies kernal manipulation to input image, -1 is default for ddepth and matches input
    self.input_image = cv2.filter2D(self.input_image, -1, kernel_sharpen)
   
  
  # Identify image contours and approximate them to remove unwanted noise
  # @param minArea defines minimum component size to rule out insignifcantly small contour shapes
  # @return Rectangle representation of component contours
  def findContourRectangle(self, minArea):
    # Contours are curves that join all continuous points along a boundary with same color/intensity
    # findContours specifically searches for white objects on a black background, must be binary img
    # findCountours (src, contour retrieval mode, contour approximation method)
    # A copy of input image is used to preserve original image, because findContours would alter image
    # cv2.CHAIN_APPROX_SIMPLE removed redundant points to reduce size of contours and save memory
    _, contours, _= cv2.findContours(self.binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    self.componentsFound = 0
    # Examine each contour detected in image
    for c in contours:
      #if area of contours is greater than min target area
      if cv2.contourArea(c) > minArea:
        # Calculates perimeter of contour c
        # arcLength(input contour, closed contour)
        perimeter = cv2.arcLength(c, True)
        # Approximate shape and remove noise using approxPolyDP(contour, epsilon, closed contour)
        # Value for epsilon should be adjusted to fine tune component's shape approximation
        # epsilon = 10% of perimiter
        epsilon = perimeter*0.1
        approxShape = cv2.approxPolyDP(c, epsilon, True)
        # Check if shape has has 4 edges
        if len(approxShape) == 4:
          # increase total number of components found
          # this should always be 1 if viewing image of component
          self.componentsFound += 1
          # Create a rotated rectangle that bounds the approximated shape
          # minAreaRect(InputArray points) finds a rotated rectangle of the minimum area
          # that is enclosed by 2D point set approxShape
          minRect = cv2.minAreaRect(approxShape)
          return minRect
    # Return null if no components were found 
    return None
          
  # Draw a min area fitted rectangle around contours
  # Rectangle = min area rectangle representation of approximated contours
  # Rectangle is defined by findContourRectangle()
  def drawContoursFromRectangle(self, rect):
    # boxPoints finds four vertices of a rotated rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # drawContours(image to draw on, contours to draw, index of contour to draw, color, and thickness
    cv2.drawContours(self.input_image, [box], 0,(255, 0, 0), 1)

  # Adjust angle of rotation detected on component rectangle
  # We want 0 def, not 90 deg or 180 deg
  # @return double angle
  def normalizeRectangle(self, angle):
    while(angle < -45 or angle > 45):
      angle += 90
      angleStr = str(angle)
    return angle
  
  # Draw pixel values of center (x,y) , dimensions (w,h) , and angle of rotation
  def drawRectangleDetails(self, rect):
    # rect[0] contains center of rectangle position
    # Get position, format to 3 decimal, cast to String
    centerX, centerY = rect[0]
    centerX = str(format(centerX, '.3f'))
    centerY = str(format(centerY, '.3f'))
    # rect[1] contains dimensions
    # get dimensions, format to 3 decimal, and cast to String
    dimension1, dimension2 = rect[1]
    dimension1 = str(format(dimension1, '.3f'))
    dimension2 = str(format(dimension2, '.3f'))
    # rect[2] contains angle of rotation
    # get angle, normalize angle of rotation, format to 3 decimal, and cast to String
    angle = self.normalizeRectangle(rect[2])
    angle = str(format(angle, '.3f'))
    # Set font and apply text to output image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(self.input_image, 'Center: ' + centerX + ', ' + centerY, (10, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(self.input_image, "Dimensions: " + dimension1 + ', ' + dimension2, (10, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(self.input_image, "Angle of Rotation: " + angle, (10, 60), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
  
  # Return string that contains component's center coordinates (x,y) and it's angle of rotation
  def getRectangleDetails(self, rect):
    centerX, centerY = rect[0]
    orientationDetails = "X" + str(format(centerX, '.3f')) + ", Y" + str(format(centerY, '.3f')) + ", "
    angle = self.normalizeRectangle(rect[2])
    orientationDetails += str(format(angle, '.3f'))
    return orientationDetails
  
  # Display output image to user and give user option to save
  # Close all windows on completion
  def displayOutput(self):
    cv2.imshow("Output", self.input_image)
    k = cv2.waitKey() & 0XFF
    # If 's' key stroke, save image with timestamp.jpg as filename
    if k == ord('s'):
      timestamp = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
      cv2.imwrite(timestamp, self.input_image)
      cv2.destroyAllWindows()
    else:
      cv2.destroyAllWindows()
      

if __name__ == "__main__":
  print("ComponentTracker.py is not intended to be run as 'main'")