
# Claim: KLF4 is necessary for VSMCs to gain genetic characteristics of other cell types within atherosclerotic lesions.
# The simulation will model the role of KLF4 in VSMCs and its impact on the transition to other cell types in atherosclerotic lesions.

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

class VSMC(GameObject):
    def __init__(self, name, KLF4_active=True):
        super().__init__(name)
        self.properties = {
            "KLF4_active": KLF4_active,
            "cell_type": "VSMC",
            "transitions": []
        }

    def transition(self):
        if self.properties["KLF4_active"]:
            self.properties["transitions"].append("macrophage-like")
            self.properties["transitions"].append("MSC-like")
        else:
            self.properties["transitions"].append("none")

    def makeDescriptionStr(self):
        description = f"{self.name}, KLF4 active: {self.properties['KLF4_active']}, transitions: {self.properties['transitions']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("atherosclerotic_lesion")
        vsmc_with_KLF4 = VSMC("VSMC_with_KLF4", KLF4_active=True)
        vsmc_without_KLF4 = VSMC("VSMC_without_KLF4", KLF4_active=False)
        world.addObject(vsmc_with_KLF4)
        world.addObject(vsmc_without_KLF4)
        return world

    def run_simulation(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.transition()

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
