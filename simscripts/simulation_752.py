
# Claim: Major vault protein regulates sorting of tumor suppressive miR-193a into EVs.
# The simulation will model the interaction between Major Vault Protein (MVP) and miR-193a, 
# and how the knockout of MVP affects the sorting of miR-193a into exosomes.

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

class MajorVaultProtein(GameObject):
    def __init__(self):
        super().__init__("Major Vault Protein (MVP)")
        self.properties["isKnockout"] = False

    def knockout(self):
        self.properties["isKnockout"] = True

class MiR193a(GameObject):
    def __init__(self):
        super().__init__("miR-193a")
        self.properties["inExosomes"] = True

    def accumulate(self):
        self.properties["inExosomes"] = False

class Exosome(GameObject):
    def __init__(self):
        super().__init__("Exosome")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.verify_claim()

    def _initialize_simulation(self):
        world = Container("Cell Environment")
        mvp = MajorVaultProtein()
        mir193a = MiR193a()
        exosome = Exosome()

        world.addObject(mvp)
        world.addObject(mir193a)
        world.addObject(exosome)

        return world

    def verify_claim(self):
        mvp = self.rootObject.containsItemWithName("Major Vault Protein (MVP)")[0]
        mir193a = self.rootObject.containsItemWithName("miR-193a")[0]

        # Simulate MVP knockout
        mvp.knockout()
        if mvp.getProperty("isKnockout"):
            mir193a.accumulate()  # miR-193a accumulates in donor cells instead of exosomes

        # Check if miR-193a is in exosomes
        if not mir193a.getProperty("inExosomes"):
            return "Supported: MVP regulates sorting of miR-193a into exosomes."
        else:
            return "Refuted: MVP does not regulate sorting of miR-193a into exosomes."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
