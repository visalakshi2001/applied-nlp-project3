
# Claim: Pre-mRNAs associated with spliceosomal components are less stable than unassociated splicing substrates.
# The simulation will compare the stability of pre-mRNAs associated with spliceosomal components versus unassociated splicing substrates.

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

class PreMRNA(GameObject):
    def __init__(self, name, stability):
        super().__init__(name)
        self.properties["stability"] = stability

    def tick(self):
        # Simulate degradation over time
        self.properties["stability"] -= 1

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("RNA Environment")
        associated_mRNA = PreMRNA("Associated pre-mRNA", stability=5)  # Less stable
        unassociated_mRNA = PreMRNA("Unassociated pre-mRNA", stability=10)  # More stable
        world.addObject(associated_mRNA)
        world.addObject(unassociated_mRNA)
        return world

    def run_simulation(self):
        for _ in range(5):  # Simulate for 5 time steps
            for obj in self.rootObject.getAllContainedObjectsRecursive():
                obj.tick()

    def check_stability(self):
        associated = self.rootObject.containsItemWithName("Associated pre-mRNA")[0]
        unassociated = self.rootObject.containsItemWithName("Unassociated pre-mRNA")[0]
        if associated.getProperty("stability") < unassociated.getProperty("stability"):
            return "Claim Supported: Associated pre-mRNAs are less stable."
        else:
            return "Claim Refuted: Associated pre-mRNAs are not less stable."

def main():
    simulation = Simulation()
    result = simulation.check_stability()
    print(result)

if __name__ == "__main__":
    main()
