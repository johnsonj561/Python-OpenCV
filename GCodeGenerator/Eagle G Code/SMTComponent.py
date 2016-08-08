#Justin Johnson Summer 2016
#SMTComponent Class
#Accepts List of SMT Component attributes
class SMTComponent(object):
  #constructor 
  #@param attributeList list of component's attributes
  def __init__(self, attributeList):
    self.attribute_list = attributeList
    self.attribute_titles = []
    #Default SMT Component has unknown attribute titles
    #So we will assign integer values to each title
    for i, attribute in enumerate(attributeList):
      self.attribute_titles.append(i)
  
  #@return list of component's attributes
  def getAttributeList(self):
    return self.attribute_list
  
  def getAttributeTitles(self):
    return self.attribute_titles
  
  #Print component attributes, each attribute on new line
  def printComponent(self):
    i = 0
    for attribute in self.attribute_list:
      print(str(self.attribute_titles[i]) + ": " + str(attribute))
      i += 1
  
if __name__ == "__main__":
  print("SMTComponent main()")


  
  
  