import re
import os.path

class CentroidParser():
  #constructor 
  #@param input_file path of text file to be parsed (centroid output file *.mnt)
  def __init__(self, input_file):
    self.input_path = input_file
    #verify valid path for input file
    assert os.path.isfile(self.input_path), "Invalid Input Path, Unable To Parse File " + input_file
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
      
  #Close file stream
  def closeCentroidParser(self):
    self.input_file.close()
    
  #Parses a line of text that contains component attributes
  #Accepts white space and comma delimited attributes
  #@param component line of text containing component attributes
  #@param attributeCount total number of attributes to parse
  #@return list of component attributes
  def parseComponentAttributes(self, component, attributeCount):
    #initialize list to store component attributes
    attributeList = []
    #Replace commas with white space, then split component attributes by whitespace
    #Currently compatible with both Eagle and Altium centroid files
    component = component.replace(",", " ")
    attributes = component.split()
    #attributes = re.split("[ ,]+", component, attributeCount)  
    for attribute in attributes:
      attributeList.append(attribute)
    return attributeList
    
    
if __name__ == "__main__":
  print("CentroidParser main() - CentroidParser is not intended to be run as main()")


  
  
  