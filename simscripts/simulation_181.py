
# Claim: Blocking the interaction between TDP-43 and respiratory complex I proteins ND3 and ND6 prevents TDP-43-induced neuronal loss.
# The simulation will model the interaction between TDP-43 and mitochondrial proteins ND3 and ND6, and the effect of blocking this interaction on neuronal loss.

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

class TDP43(GameObject):
    def __init__(self, name, mitochondrial_localization=True):
        super().__init__(name)
        self.properties = {
            "mitochondrial_localization": mitochondrial_localization,
            "neuronal_loss": False
        }

    def tick(self):
        if self.getProperty("mitochondrial_localization"):
            self.properties["neuronal_loss"] = True  # Simulate neuronal loss if TDP-43 is localized in mitochondria
        else:
            self.properties["neuronal_loss"] = False  # No neuronal loss if localization is blocked

class NDComplex(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        tdp43 = TDP43("TDP-43")
        nd_complex = NDComplex("Respiratory Complex I (ND3 and ND6)")
        world.addObject(tdp43)
        world.addObject(nd_complex)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "block interaction": ["block", "TDP-43"],
            "allow interaction": ["allow", "TDP-43"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "block":
            tdp43 = self.rootObject.containsItemWithName("TDP-43")[0]
            tdp43.properties["mitochondrial_localization"] = False
            self.observationStr = "Blocked TDP-43 mitochondrial localization."
        elif actionVerb == "allow":
            tdp43 = self.rootObject.containsItemWithName("TDP-43")[0]
            tdp43.properties["mitochondrial_localization"] = True
            self.observationStr = "Allowed TDP-43 mitochondrial localization."

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    actions = ["look", "block interaction", "look", "allow interaction", "look"]
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)

    # Check the final state of TDP-43 to determine if the claim is supported or refuted
    tdp43 = simulation.rootObject.containsItemWithName("TDP-43")[0]
    if tdp43.getProperty("neuronal_loss"):
        print("Claim Refuted: Neuronal loss occurred.")
    else:
        print("Claim Supported: No neuronal loss occurred.")

if __name__ == "__main__":
    main()
