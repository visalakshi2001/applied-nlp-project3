
# Claim: Two variants of chromosome 6q21 are associated with radiation therapy-induced second malignancies in pediatric Hodgkin lymphoma patients.
# The simulation will check if the identified variants at chromosome 6q21 are indeed associated with second malignant neoplasms (SMNs) in pediatric Hodgkin lymphoma patients.

class GameObject():
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            return
        self.constructorsRun = ["GameObject"]
        self.name = name
        self.parent = None
        self.contains = []
        self.properties = {}

    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent != None:
            self.parent.removeObject(self)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    def containsItemWithName(self, name):
        foundObjects = []
        for obj in self.contains:
            if obj.name == name:
                foundObjects.append(obj)
        return foundObjects

    def tick(self):
        pass

    def makeDescriptionStr(self):
        return self.name

class Container(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return
        GameObject.__init__(self, name)
        self.constructorsRun.append("Container")
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"

    def openContainer(self):
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be opened.", False)
        if self.getProperty("isOpen"):
            return ("The " + self.name + " is already open.", False)
        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    def closeContainer(self):
        if not (self.getProperty("isOpenable") == True):
            return ("The " + self.name + " can't be closed.", False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is already closed.", False)
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

    def placeObjectInContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)
        if not (obj.getProperty("isMoveable") == True):
            return ("The " + obj.name + " is not moveable.", None, False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)
        if not obj.getProperty("isMoveable"):
            return ("The " + obj.name + " is not moveable.", None, False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

class Variant(GameObject):
    def __init__(self, name, associated_with_SMN=False):
        super().__init__(name)
        self.properties = {
            "associated_with_SMN": associated_with_SMN
        }

    def tick(self):
        pass

    def makeDescriptionStr(self):
        description = f"A variant named {self.name}, associated with SMN: {self.properties['associated_with_SMN']}."
        return description

class Patient(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.variants = []

    def addVariant(self, variant):
        self.variants.append(variant)

    def checkVariants(self):
        for variant in self.variants:
            if variant.getProperty("associated_with_SMN"):
                return True
        return False

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.checkClaim()

    def _initialize_simulation(self):
        world = World()
        patient = Patient("pediatric_hodgkin_lymphoma_patient")
        
        # Creating two variants at chromosome 6q21
        variant1 = Variant("variant_1", associated_with_SMN=True)
        variant2 = Variant("variant_2", associated_with_SMN=True)
        
        patient.addVariant(variant1)
        patient.addVariant(variant2)
        
        world.addObject(patient)
        return world

    def checkClaim(self):
        patient = self.rootObject.contains[0]  # Get the patient object
        if patient.checkVariants():
            return "Supported: The claim is verified as true."
        else:
            return "Refuted: The claim is false."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
