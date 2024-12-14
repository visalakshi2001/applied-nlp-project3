
# Claim: Deltex has no known interactions with eIF3f.
# The simulation will check if eIF3f interacts with Deltex based on the provided reference text.

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
        return self.properties.get(propertyName, None)

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent is not None:
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
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be closed.", False)
        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is already closed.", False)
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

    def placeObjectInContainer(self, obj):
        if not self.getProperty("isContainer"):
            return ("The " + self.name + " can't hold objects.", False)
        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not self.getProperty("isContainer"):
            return ("The " + self.name + " can't hold objects.", None, False)
        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

class Protein(GameObject):
    def __init__(self, name, interacts_with=None):
        super().__init__(name)
        self.interacts_with = interacts_with

    def makeDescriptionStr(self):
        return f"{self.name} interacts with: {self.interacts_with if self.interacts_with else 'nothing'}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("cell")
        deltex = Protein("Deltex")
        eIF3f = Protein("eIF3f", interacts_with="Notch")  # eIF3f interacts with Notch, not Deltex
        world.addObject(deltex)
        world.addObject(eIF3f)
        return world

    def check_interaction(self):
        eIF3f = self.rootObject.containsItemWithName("eIF3f")[0]
        if eIF3f.interacts_with == "Deltex":
            return "Claim Refuted: eIF3f interacts with Deltex."
        else:
            return "Claim Supported: eIF3f does not interact with Deltex."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_interaction()
    print(result)

if __name__ == "__main__":
    main()
