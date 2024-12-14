
# Claim: Normal granulomas form in the absence of TNF in Zebrafish.
# The simulation will test the claim by modeling the effects of TNF absence on granuloma formation in zebrafish.

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

class Granuloma(GameObject):
    def __init__(self, name, tnf_present=True):
        super().__init__(name)
        self.properties = {
            "tnf_present": tnf_present,
            "is_formed": False,
            "macrophage_health": 100
        }

    def tick(self):
        if not self.properties["tnf_present"]:
            self.properties["is_formed"] = True
            self.properties["macrophage_health"] -= 10  # Simulating macrophage stress due to absence of TNF

    def makeDescriptionStr(self):
        description = f"A granuloma named {self.name}, TNF present: {self.properties['tnf_present']}, "
        description += f"formed: {self.properties['is_formed']}, macrophage health: {self.properties['macrophage_health']}."
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
        granuloma = Granuloma("granuloma_1", tnf_present=False)  # Simulating absence of TNF
        world.addObject(granuloma)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

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

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the state of the granuloma to determine if the claim is supported or refuted
    granuloma = simulation.rootObject.containsItemWithName("granuloma_1")[0]
    if granuloma.properties["is_formed"]:
        print("Claim Supported: Normal granulomas form in the absence of TNF.")
    else:
        print("Claim Refuted: Normal granulomas do not form in the absence of TNF.")

if __name__ == "__main__":
    main()
