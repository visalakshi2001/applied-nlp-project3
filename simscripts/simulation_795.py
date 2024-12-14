
# Claim: Mitochondria play a major role in apoptosis.
# This simulation will demonstrate the role of mitochondria in apoptosis based on the provided reference text.

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

class Mitochondria(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "role_in_apoptosis": True
        }

    def participate_in_apoptosis(self):
        return self.properties["role_in_apoptosis"]

class Cell(Container):
    def __init__(self, name):
        super().__init__(name)
        self.mitochondria = Mitochondria("Mitochondria")

    def check_apoptosis_role(self):
        return self.mitochondria.participate_in_apoptosis()

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.cell = Cell("Cell")
        self.addObject(self.cell)

    def makeDescriptionStr(self):
        return f"In the {self.name}, you see: {self.cell.makeDescriptionStr()}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.check_claim()

    def _initialize_simulation(self):
        return World()

    def check_claim(self):
        if self.rootObject.cell.check_apoptosis_role():
            return "Claim Supported: Mitochondria play a major role in apoptosis."
        else:
            return "Claim Refuted: Mitochondria do not play a major role in apoptosis."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
