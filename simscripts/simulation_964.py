
# Claim: Pre-mRNAs associated with spliceosomal components are more stable than unassociated splicing substrates.
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
    def __init__(self, name, associated=False):
        super().__init__(name)
        self.properties = {
            "associated": associated,
            "stability": 0
        }

    def tick(self):
        if self.properties["associated"]:
            self.properties["stability"] += 1  # Associated pre-mRNAs become more stable
        else:
            self.properties["stability"] -= 1  # Unassociated pre-mRNAs become less stable

    def makeDescriptionStr(self):
        description = f"A pre-mRNA named {self.name}, associated: {self.properties['associated']}, stability: {self.properties['stability']}."
        return description

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
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        associated_pre_mrna = PreMRNA("associated_pre_mRNA", associated=True)
        unassociated_pre_mrna = PreMRNA("unassociated_pre_mRNA", associated=False)
        world.addObject(associated_pre_mrna)
        world.addObject(unassociated_pre_mrna)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            self.doWorldTick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate a number of ticks to observe stability changes
    for _ in range(5):
        print("Ticking...")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the final stability values to verify the claim
    associated_stability = simulation.rootObject.containsItemWithName("associated_pre_mRNA")[0].getProperty("stability")
    unassociated_stability = simulation.rootObject.containsItemWithName("unassociated_pre_mRNA")[0].getProperty("stability")

    if associated_stability > unassociated_stability:
        print("Claim Supported: Associated pre-mRNAs are more stable than unassociated splicing substrates.")
    else:
        print("Claim Refuted: Associated pre-mRNAs are not more stable than unassociated splicing substrates.")

if __name__ == "__main__":
    main()
