import cv2
import numpy as np

class EdgeSharpener():
  def __init__(self, input_img):
    self._input_image = cv2.imread(input_img, 0)
    cv2.imshow('Original Img', self._input_image)


  def sharpenImage(self, output_file):
    #generate kernal to be applied to image
    kernel_sharpen = np.array([[-1, -1, -1, -1, -1],
                               [-1, 2, 2, 2, -1],
                               [-1, 2, 8, 2, -1],
                               [-1, 2, 2, 2, -1],
                               [-1, -1, -1, -1, -1]]) / 8.0
    output_img = cv2.filter2D(self._input_image, -1, kernel_sharpen)
    cv2.imshow('Output', output_img)
    c = cv2.waitKey(0) & 0xFF
    if c == ord('s'):
      cv2.imwrite(output_file, output_img)
      cv2.destroyAllWindows()
    elif c == 27:
      cv2.destroyAllWindow()
      
    
      
      