#Justin Johnson Summer 2016
#Testing SMTComponent Class 
#Populate component objects from list of components

from CentroidParser import CentroidParser
from SMTComponent import SMTComponent
import argparse

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
  
  #parse componentAttributes
  componentAttributes = mCentroidParser.parseComponentAttributes(componentList[0], 6)
  
  #create SMTComponent object from above component's attribute list
  print("\nCreating a new SMTComponent object that stores attributes of 1st component in centroid file")
  mSMTComponent = SMTComponent(componentAttributes)
  print("\nPrinting SMTComponent object\n")
  mSMTComponent.printComponent()
  
  #change component description
  print("\nChanging component description to 'NewDescription'")
  mSMTComponent.setDescription("NewDescription")
  print("\nPrinting SMTComponent object/")
  mSMTComponent.printComponent()
  
  #print x and y coordinates only
  print("\nPrinting X and Y Coordinates using getter methods\n")
  print("x: " + str(mSMTComponent.getXCoordinate()))
  print("y: " + str(mSMTComponent.getYCoordinate()))
  
  
if __name__ == "__main__":
  main()