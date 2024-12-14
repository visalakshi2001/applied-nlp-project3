
# Claim: The most prevalent adverse events to Semaglutide are gastrointestinal.
# Simulation to verify the claim based on the provided reference text.

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

class AdverseEvent(GameObject):
    def __init__(self, name, prevalence):
        super().__init__(name)
        self.properties["prevalence"] = prevalence

    def makeDescriptionStr(self):
        return f"{self.name} with prevalence: {self.properties['prevalence']}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("environment")
        gastrointestinal_event = AdverseEvent("Gastrointestinal Events", "most common")
        other_event = AdverseEvent("Other Adverse Events", "less common")
        world.addObject(gastrointestinal_event)
        world.addObject(other_event)
        return world

    def step(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    result = simulation.step()
    print(result)

    # Check if the claim is supported or refuted
    if "Gastrointestinal Events" in result and "most common" in result:
        print("Claim Supported: The most prevalent adverse events to Semaglutide are gastrointestinal.")
    else:
        print("Claim Refuted: The claim about gastrointestinal events being the most prevalent is not supported.")

if __name__ == "__main__":
    main()
