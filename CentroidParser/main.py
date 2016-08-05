#Justin Johnson Summer 2016
#Parsing Eagle layout's centroid output file for pick and place machine
#Print Component List and Attributes to console
#CentroidParser generates lists of components and component attributes

#Next step will be to create ComponentDescriptor class that stores attributes
#for each component. We will then create a list of ComponentDescriptor objects
#that will represent all components of PCB Design. Pick and place machine will
#iterate through list and place components


from CentroidParser import CentroidParser
import argparse
import re 

def main():
  #configure argument parser to read path to input file
  ap = argparse.ArgumentParser()
  ap.add_argument("-f", "--file", help = "path to file being parsed")
  #parse arguments
  args = vars(ap.parse_args())
  input_file = args["file"]
  
  #Create CentroidParser object
  mCentroidParser = CentroidParser(input_file)
  
  #generate list that contains all components found in centroid file
  componentList = mCentroidParser.getComponentList()
  
  #get list of attribute titles to display to console
  attributeTitles = mCentroidParser.getAttributeTitles()
  
  #print each component's attribute values
  for component in componentList:
    i = 0
    #print attribute title: attribute value
    attributes = mCentroidParser.parseComponentAttributes(component, 6)
    for attribute in attributes:
      print(attributeTitles[i] + ": " + attribute)
      i += 1
  
if __name__ == "__main__":
  main()