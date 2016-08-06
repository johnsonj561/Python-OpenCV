from EagleSMTComponent import EagleSMTComponent
from CentroidParser import CentroidParser
import argparse

#Generate a list of SMTComponent objects derived from PCB Design Centroid File
def generateComponentObjectList(input_file):
  #Create CentroidParser object
  mCentroidParser = CentroidParser(input_file)
  #generate list that contains all components found in centroid file
  #each element of list consists of string which contains attributes of component
  components = mCentroidParser.getComponentList()
  #declare array to store the EagleSMTComponent Objects
  componentObjectList = []
  #create a EagleSMTComponent instance for every component and append to componentObjectList[]
  for component in components:
    attributes = mCentroidParser.parseComponentAttributes(component, 6)
    componentObjectList.append(EagleSMTComponent(attributes))  
  return componentObjectList
  
#moveToPart generates G Code that moves PnP head linearly to part with corresponding package ID
def moveToPart(package_id)

#pickUpPart generates G Code to lower head, turn on vacuum nozzle, and raise head
def pickUpPart()

#placepart generates G Code to lower head, turn off vacuum nozzle, and raise head
def placePart()
  
def main():
  #configure argument parser to read path to input file
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--centroid", help = "path to centroid file being parsed")
  ap.add_argument("-p", "--parts", help = "path to file containing part information and location")
  ap.add_argument("-o", "--output", help = "path to output G-Code file")
  args = vars(ap.parse_args())
  input_file = args["centroid"]
  parts_file = args["parts"]
  outout_file = args["output"]
  
  #generate list of SMTComponent objects to be placed
  componentObjectList = generateComponentObjectList(input_file)
  
  #generate parts list of SMTComponent objects
  partsObjectList = generateComponentObjectList(parts_file)
  
  for component in componentObjectList:
    component.printComponent()
  
  
  counter = 0
  
  #traverse array of component objects and write move commmands to output file
  for component in componentObjectList:
    couner += 1
    print("\n\nMoving To Part " + str(counter))
    #pick up part
    moveToPart(component.getPackage())
    print("Picking Up Part " + str(counter))
    pickUpPart()
    print("Moving To Placement Location of Part " + str(counter))
    moveToLocation(component.getXCoordinate(), component.getYCoordinate())
    print("At Location (" + str(component.getXcoordinate()) + ", " + str(component.getYCoordinate()) + ")")
    print("Placing Part " + str(counter))
    placePart()
    
  

  
  
  
if __name__ == "__main__":
  main()