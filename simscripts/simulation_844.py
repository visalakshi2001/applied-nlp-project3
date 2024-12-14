
# Claim: Neutrophil extracellular trap (NET) antigens may contain the targeted autoantigens PR3 and MPO.
# The simulation will verify if NETs contain PR3 and MPO as stated in the reference text.

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

class Antigen(GameObject):
    def __init__(self, name):
        super().__init__(name)

class NET(GameObject):
    def __init__(self):
        super().__init__("Neutrophil Extracellular Trap (NET)")
        self.contains = [Antigen("Proteinase-3 (PR3)"), Antigen("Myeloperoxidase (MPO)")]

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("environment")
        net = NET()
        world.addObject(net)
        return world

    def checkClaim(self):
        net = self.rootObject.contains[0]  # Get the NET object
        antigens = [antigen.name for antigen in net.contains]
        if "Proteinase-3 (PR3)" in antigens and "Myeloperoxidase (MPO)" in antigens:
            return "Claim Supported: NETs contain PR3 and MPO."
        else:
            return "Claim Refuted: NETs do not contain PR3 and MPO."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.checkClaim()
    print(result)

if __name__ == "__main__":
    main()
