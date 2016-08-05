import re

class CentroidParser():
  #constructor 
  #@param input_file path of text file to be parsed (centroid output file *.mnt)
  def __init__(self, input_file):
    self.input_path = input_file
    self.attribute_titles = ["PartDes", "x", "y", "rotation", "value", "package"]
    try:
      self.input_file = open(self.input_path)
    except IOError:
      print("Constructor: Unable to open file.")
       
        
  #@return path to file being read
  def getInputPath(self):
    return self.input_path   
  
  #@return file object to be parsed
  def getInputFile(self):
    return self.input_file
  
  #@return list of component descriptors
  def getComponentList(self):
    return self.input_file.readlines()
  
  #@return list that contains title of component attributes
  def getAttributeTitles(self):
    #array that displays component description heading
    return self.attribute_titles

  #Resets file iterator to beginning by creating new file object
  def resetFileIterator(self):
    try:
      self.input_file.close()
    except IOError:
      print("In resetFileIterator: Unable to close input file.")
    try:
      self.input_file = open(self.input_path)
    except IOError:
      print("In resetFileIterator: Unable to re-open input file.")
    
  #Parses a line of text that contains component attributes
  #Accepts white space and comma delimited attributes
  #@param component line of text containing component attributes
  #@param attributeCount total number of attributes to parse
  #@return list of component attributes
  def parseComponentAttributes(self, component, attributeCount):
    #initialize list to store component attributes
    attributeList = []
    #Use regex to split component attributes
    attributes = re.split("[ ,]+", component, attributeCount)  
    for attribute in attributes:
      attributeList.append(attribute)
    return attributeList
    
    
if __name__ == "__main__":
  print("CentroidParser main()")


  
  
  