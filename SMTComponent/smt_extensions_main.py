#Justin Johnson Summer 2016
#Testing SMTComponent Class 
#Populate component objects from list of components, testing both Altium and Eagle extensions

from CentroidParser import CentroidParser
from SMTComponent import SMTComponent
from EagleSMTComponent import EagleSMTComponent
from AltiumSMTComponent import AltiumSMTComponent
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
  
  #create SMTComponent object and print
  mSMTComponent = SMTComponent(componentAttributes)
  mSMTComponent.printComponent()
  
  #create EagleSMTComponent object and print
  mEagleSMTComponent = EagleSMTComponent(componentAttributes)
  mEagleSMTComponent.printComponent()
  print("\nTESTING EagleSMTComponent Methods")
  print("Changing description")
  mEagleSMTComponent.setDescription("Hello")
  print("Changing X Coordinate")
  mEagleSMTComponent.setXCoordinate(55)
  print("Changing Y Coordinate")
  mEagleSMTComponent.setYCoordinate(89)
  print("Changing Rotation")
  mEagleSMTComponent.setRotation(-45)
  print("Changing value")
  mEagleSMTComponent.setValue(1550)
  print("Changing package name")
  mEagleSMTComponent.setPackage("NewPackage")
  print("\nReprinting component attributes\n")
  mEagleSMTComponent.printComponent()
  print("\nPrinting component attributes using getter methods")
  print(mEagleSMTComponent.getDescription())
  print(mEagleSMTComponent.getXCoordinate())
  print(mEagleSMTComponent.getYCoordinate())
  print(mEagleSMTComponent.getRotation())
  print(mEagleSMTComponent.getValue())
  print(mEagleSMTComponent.getPackage())
      
  #create an AltiumSMTComponent object and print
  #parse componentAttributes
  componentAttributes = mCentroidParser.parseComponentAttributes(componentList[1], 6)
  mAltiumSMTComponent = AltiumSMTComponent(componentAttributes)
  mAltiumSMTComponent.printComponent()
  print("\nTESTING AltiumSMTComponent Methods")
  print("Changing reference designator")
  mAltiumSMTComponent.setDesignator("World")
  print("Changing X Coordinate")
  mAltiumSMTComponent.setXCoordinate(90)
  print("Changing Y Coordinate")
  mAltiumSMTComponent.setYCoordinate(140)
  print("Changing Board Side")
  mAltiumSMTComponent.setBoardSide("bottom")
  print("Changing Rotation")
  mAltiumSMTComponent.setRotation(113)
  print("Changing part name")
  mAltiumSMTComponent.setPartName("My New Part Name")
  print("\nReprinting component attributes\n")
  mAltiumSMTComponent.printComponent()
  print("\nPrinting component attributes using getter methods")
  print(mAltiumSMTComponent.getDesignator())
  print(mAltiumSMTComponent.getXCoordinate())
  print(mAltiumSMTComponent.getYCoordinate())
  print(mAltiumSMTComponent.getBoardSide())
  print(mAltiumSMTComponent.getRotation())
  print(mAltiumSMTComponent.getPartName())
  
if __name__ == "__main__":
  main()