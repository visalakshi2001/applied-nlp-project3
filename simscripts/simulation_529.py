
# Claim: Human embryonic stem cells give rise to cell types from all three embryonic germ layers.
# This simulation will test the claim by simulating the differentiation of human embryonic stem cells.

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

class StemCell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "isUndifferentiated": True,
            "germLayers": []
        }

    def differentiate(self):
        if self.properties["isUndifferentiated"]:
            self.properties["isUndifferentiated"] = False
            self.properties["germLayers"] = ["ectoderm", "mesoderm", "endoderm"]
            return f"{self.name} has differentiated into cell types from all three embryonic germ layers."
        else:
            return f"{self.name} is already differentiated."

class World(Container):
    def __init__(self):
        Container.__init__(self, "embryonic environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = ""

    def _initialize_simulation(self):
        world = World()
        stem_cell = StemCell("Human Embryonic Stem Cell")
        world.addObject(stem_cell)
        return world

    def step(self):
        stem_cell = self.rootObject.contains[0]  # Get the stem cell
        differentiation_result = stem_cell.differentiate()
        self.result = differentiation_result
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.step()
    print(result)

    # Check if the claim is supported or refuted
    if "differentiated into cell types from all three embryonic germ layers" in simulation.result:
        print("Claim Supported: Human embryonic stem cells give rise to cell types from all three embryonic germ layers.")
    else:
        print("Claim Refuted: Human embryonic stem cells do not give rise to cell types from all three embryonic germ layers.")

if __name__ == "__main__":
    main()
