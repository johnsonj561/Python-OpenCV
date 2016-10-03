#PNP Computer Vision System for identifying ICs and analyzing IC orientation
#Justin Johnson
#Fall 2016
import numpy as np
import cv2
import time

#ComponentTracker class accepts input image path and provides functionality:
#Preprocessing, identify countours, drawing best fit rectangle and return orientation attributes
class ComponentTracker():
  #constructor
  #read input image path to be processed
  def __init__(self, input_image):
    self.input_image = cv2.imread(input_image)
  
  #threshold image and generate binary output image
  #@param int l = lower bound of threshold
  #@param int h = upper bound of threshold
  #@param boolean showImage displays image if true, default false
  def thresholdImage(self, l, h, showImage = False):
    lower = np.array([l, l, l])
    upper = np.array([h, h, h])
    self.binary_image = cv2.inRange(self.input_image, lower, upper)
    if showImage:
      cv2.imshow("Thresholded Output", self.binary_image)
    
  #identify image contours and approximate them to remove unwanted noise
  #@param minArea defines minimum component size to rule out insignifcantly small contours
  #@return Rectangle representation of component contours
  def findContourRectangle(self, minArea):
    _, contours, _= cv2.findContours(self.binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    self.componentsFound = 0
    for c in contours:
      #if area of contours is greater than min target area
      if cv2.contourArea(c) > minArea:
        peri = cv2.arcLength(c, True)
        approxShape = cv2.approxPolyDP(c, 0.1*peri, True)
        #if contour has 4 sides it is a component
        if len(approxShape) == 4:
          #increase total number of components found
          #this should always be 1 if viewing image of component
          self.componentsFound += 1
          #we will create a rotated rectangle that bounds contour/shape
          minRect = cv2.minAreaRect(approxShape)
          return minRect
    #if we did not find rectangle, return null    
    return None
          
  #draw a min area fitted rectangle around contours
  #rectangle = min area rectangle representation of approx contours
  def drawContoursFromRectangle(self, rect):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(self.input_image, [box], 0,(255, 0, 0), 1)

  #adjust angle of rotation detected on component rectangle
  #we want 0 def, not 90 deg or 180 deg
  #@return double angle
  def normalizeRectangle(self, angle):
    while(angle < -45 or angle > 45):
      angle += 90
      angleStr = str(angle)
      print "Angle detected in normalizRectangle(): " + angleStr
    return angle
  
  #draw pixel values of center (x,y) , dimensions (w,h) , and angle of rotation
  def drawRectangleDetails(self, rect):
    #rect[0] contains center of rectangle position
    #get position, format to 3 decimal, cast to String
    centerX, centerY = rect[0]
    centerX = str(format(centerX, '.3f'))
    centerY = str(format(centerY, '.3f'))
    #rect[1] contains dimensions
    #get dimensions, format to 3 decimal, and cast to String
    dimension1, dimension2 = rect[1]
    dimension1 = str(format(dimension1, '.3f'))
    dimension2 = str(format(dimension2, '.3f'))
    #rect[2] contains angle of rotation
    #get angle, normalize angle of rotation format to 3 decimal,and cast to String
    angle = self.normalizeRectangle(rect[2])
    angle = str(format(angle, '.3f'))
    #set font and apply text to output image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(self.input_image, 'Center: ' + centerX + ', ' + centerY, (10, 20), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(self.input_image, "Dimensions: " + dimension1 + ', ' + dimension2, (10, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(self.input_image, "Angle of Rotation: " + angle, (10, 60), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
  

  #display output image to user a long with total number of components found
  def displayOutput(self):
    cv2.imshow("Output", self.input_image)
    print("Total number of components found = : " + str(self.componentsFound))
    k = cv2.waitKey() & 0XFF
    if k == ord('s'):
      timestamp = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
      cv2.imwrite(timestamp, self.input_image)
      cv2.destroyAllWindows()
    else:
      cv2.destroyAllWindows()
      

if __name__ == "__main__":
  print("ComponentTracker.py is not intended to be run as 'main'")