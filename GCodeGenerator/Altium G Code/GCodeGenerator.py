#Justin Johnson Summer 2016
#GCodeGenerator object designed to parse Altium or Eagle Centrod Files and write G Code commands to output file
#Intended for use with Pick and Place Machine

from EagleSMTComponent import EagleSMTComponent
from AltiumSMTComponent import AltiumSMTComponent
from CentroidParser import CentroidParser

class GCodeGenerator():
  
  #define constants
  EAGLE_CENTROID_FILE = 1
  ALTIUM_CENTROID_FILE = 2
  
  #G Code Generator Constructor
  #Declares CentroidParser to create lists of components to be placed and parts in stack
  #Opens output file to write G Code commands to
  #WARNING - output_file parameter will overwrite an existing file without warning
  def __init__(self, centroid_file, centroid_type, parts_file, output_file="output.txt"):
    self.centroid_file = centroid_file
    self.centroid_type = centroid_type
    self.parts_file = parts_file
    #open output file to write G Code commands to
    try:
      self.output_file = open(output_file, "w")
    except IOError:
      print("Unable to open output file to write G Code")
    

  #Generate a list of SMTComponent objects derived from PCB Design Centroid File
  def generateComponentObjectList(self, input_file):
    #Create CentroidParser object
    mCentroidParser = CentroidParser(input_file)
    #generate list that contains all components found in centroid file
    #each element of list consists of string which contains attributes of component
    components = mCentroidParser.getComponentList()
    #declare array to store the SMTComponent Objects
    componentObjectList = []
    #create a SMTComponent instance for every component and append to componentObjectList[]
    for component in components:
      #If working with Eagle centroid file:
      if self.centroid_type == self.EAGLE_CENTROID_FILE:
        attributes = mCentroidParser.parseComponentAttributes(component, 6)
        componentObjectList.append(EagleSMTComponent(attributes))  
      #Else if working with Altium centroid file:
      elif self.centroid_type == self.ALTIUM_CENTROID_FILE:
        attributes = mCentroidParser.parseComponentAttributes(component, 11)
        componentObjectList.append(AltiumSMTComponent(attributes))  
      else: assert (1),"Centroid File Type " + self.centroid_type + " is an invalid file type" 
    #Close input centroid file once finished reading
    mCentroidParser.closeCentroidParser()
    return componentObjectList

  #Initiliaze G Code output file with start up settings
  def initializeGCode(self):
    self.output_file.write(";initializeGCode() configures start up settings. See GCodeGenerator.py to change\n")
    self.output_file.write("G21; Set units to millimeters\nG90; Set absolute coordinates\nG28 X0 Y0; Home x and y axis\n")
    self.output_file.write("G21; Set units to millimeters\nG90; Set absolute coordinates\nG28 X0 Y0; Home x and y axis\n")
    self.output_file.write("G28 Z0; Home Z axis\nG1 F3000; Set feed rate (speed) for first move\n")

  #moveToPart generates G Code that moves PnP head linearly to part with corresponding package ID
  #assert statement triggerred if package id is not found in part list, terminating program
  def moveToPart(self, component, partsObjectList):
    if self.centroid_type == self.EAGLE_CENTROID_FILE:
      component_id = component.getPackage()
      for part in partsObjectList:
        part_id = part.getPackage()
        if part_id == component_id:
          self.output_file.write("G1 X" + str(part.x_coord) + " Y" + str(part.y_coord) + "; moving to part for pick up\n")
          break
    elif self.centroid_type == self.ALTIUM_CENTROID_FILE:
      component_id = component.getDesignator()
      for part in partsObjectList:
        part_id = part.getDesignator()
        if part_id == component_id:
          self.output_file.write("G1 X" + str(part.getXCoordinate()) + " Y" + str(part.getYCoordinate()) + "; moving to part for pick up\n")
          break
    assert (1),"Package ID " + package_id + " not found in parts list"
      
  #pickUpPart generates G Code to lower head, turn on vacuum nozzle, and raise head
  #TO DO - we can programatically set the Z axis distance at run time
  def pickUpComponent(self):
    self.output_file.write("G1 Z15; Lower Z axis to component\nM10; Vacuum On\nG1 Z0; Raise Z axis to home\n")

  #placepart generates G Code to lower head, turn off vacuum nozzle, and raise head
  def lowerComponent(self):
    self.output_file.write("G1 Z15; Lower Z axis to PCB board\nM11; Vacuum Off\nG1 Z0; Raise Z axis to home\n")

  
  def moveToLocation(self, component):
    self.output_file.write("G1 X" + str(component.getXCoordinate()) + " Y" + str(component.getYCoordinate()) + "; moving to location\n")

  #Close output file when finished writing
  def closeOutputFile(self):
    self.output_file.close()
    
  #Writes string s to G Code output file
  def writeOutput(self, s):
    self.output_file.write(s)
  
    
if __name__ == "__main__":
  print("GCode Generator is not intended to be run as main()")