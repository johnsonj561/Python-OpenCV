#Justin Johnson Summer 2016
#Testing SMTComponent Class by creating instance of object and printing attributes to console

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

  
  #parse componentAttributes
  componentAttributes = mCentroidParser.parseComponentAttributes(componentList[0], 6)
  
  #create SMTComponent object from above component's attribute list
  print("\nCreating a new SMTComponent object that stores attributes of 1st component in centroid file")
  mSMTComponent = SMTComponent(componentAttributes)
  print("Printing SMTComponent object\n")
  mSMTComponent.printComponent()
  
  
if __name__ == "__main__":
  main()