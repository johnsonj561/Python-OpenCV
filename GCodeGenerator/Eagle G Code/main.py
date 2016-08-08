from GCodeGenerator import GCodeGenerator
import argparse  
  
def main():
  print("\n\nGenerating G Code Commands...\n\n")
  #configure argument parser to read path to centroid file, parts file, and output file
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--centroid", help = "path to centroid file being parsed")
  ap.add_argument("-p", "--parts", help = "path to file containing part information and location")
  ap.add_argument("-o", "--output", help = "path to output G-Code file")
  args = vars(ap.parse_args())
  centroid_file = args["centroid"]
  parts_file = args["parts"]
  output_file = args["output"]

 
  #delare G Code generator object
  mGCodeGenerator = GCodeGenerator(centroid_file, GCodeGenerator.EAGLE_CENTROID_FILE, parts_file, output_file)

  #generate list of SMTComponent objects to be placed
  componentObjectList = mGCodeGenerator.generateComponentObjectList(centroid_file)

  #generate parts list of SMTComponent objects
  partsObjectList = mGCodeGenerator.generateComponentObjectList(parts_file)
  
  #initialize G Code with start up settings
  mGCodeGenerator.initializeGCode()

  counter = 0
  #traverse array of component objects and write move commmands to output file
  for component in componentObjectList:
    counter += 1
    mGCodeGenerator.writeOutput("\n;Placing Part # " + str(counter) + "\n")
    #get the next part that needs to be placed
    mGCodeGenerator.moveToPart(component, partsObjectList)
    mGCodeGenerator.pickUpComponent()
    #if part is IC, move to light chamber for vision test
    #TO BE IMPLEMENTED
    #move to final part location for placement
    mGCodeGenerator.moveToLocation(component)
    mGCodeGenerator.lowerComponent()


  

  mGCodeGenerator.closeOutputFile()
  
  print("\nG Code Commands have been written to: " + output_file + "\n")
  
if __name__ == "__main__":
    main()