import numpy as np
import numpy as np
import cv2
import time

class ComponentTracker():
  #constructor
  #read input image path to be processed
  def __init__(self, input_image):
    self.input_image = cv2.imread(input_image)
  
  #threshold image and generate binary output image
  #l = lower bound of threshold
  #h = upper bound of threshold
  def thresholdImage(self, l, h):
    lower = np.array([l, l, l])
    upper = np.array([h, h, h])
    self.binary_image = cv2.inRange(self.input_image, lower, upper)
    cv2.imshow("Thresholded Output", self.binary_image)
    
  #identify image contours and approximate them to remove unecessary noise
  #@param minArea defines minimum component size to rule out insignifcantly small contours
  #@return Rectangle representation of component contours
  def findContourRectangle(self, minArea):
    _, contours, _= cv2.findContours(self.binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    self.total = 0
    for c in contours:
      #if area of contours is greater than min target area
      if cv2.contourArea(c) > minArea:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1*peri, True)
        #if contour has 4 sides it is a component
        if len(approx) == 4:
          #increase total number of components found
          #this should always be 1 if viewing image of component
          self.total += 1
          #we will create a rotated rectangle that bounds contour/shape
          rect = cv2.minAreaRect(approx)
          return rect
    #if we did not find rectangle, return null    
    return None
          
  #draw a min area fitted rectangle around contours
  #rectangle = min area rectangle representation of approx contours
  def drawContoursFromRectangle(self, rect):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(self.input_image, [box], 0,(255, 0, 0), 1)

    
  def normalizeRectAngle(self, angle):
    while(angle < -45 or angle > 45):
      angle += 90
    return angle
  
  #draw pixel values of center (x,y) , dimensions (w,h) , and angle of rotation
  def drawRectangleDetails(self, rect):
    center = rect[0]
    center = str(center)
    dimensions = rect[1]
    dimensions = str(dimensions)
    angle = rect[2]
    #angle = self.normalizeRectAngle(angle)
    angle = str(angle)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(self.input_image, 'Center: ' + center, (10, 50), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(self.input_image, "Dimensions: " + dimensions, (10, 70), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(self.input_image, "Angle of Rotation: " + angle, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    
    
  

  #display output image to user a long with total number of components found
  def displayOutput(self):
    cv2.imshow("Output", self.input_image)
    print("Total number of components found = : " + str(self.total))
    k = cv2.waitKey() & 0XFF
    if k == ord('s'):
      timestamp = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
      cv2.imwrite(timestamp, self.input_image)
      cv2.destroyAllWindows()
    else:
      cv2.destroyAllWindows()
      

if __name__ == "__main__":
  print("ComponentTracker.py is library and is not intended to be run as 'main'")