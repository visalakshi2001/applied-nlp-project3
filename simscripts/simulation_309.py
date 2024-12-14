
# Claim: DUSP4 increases apoptosis.
# The simulation will model the relationship between DUSP4 levels and apoptosis in a simplified manner.

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

class DUSP4(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.properties = {
            "level": level,  # Level of DUSP4
            "apoptosis_rate": 0  # Rate of apoptosis
        }

    def tick(self):
        # Apoptosis rate increases with DUSP4 level
        self.properties["apoptosis_rate"] = self.properties["level"] * 2  # Arbitrary multiplier for simulation

    def makeDescriptionStr(self):
        return f"{self.name} with DUSP4 level {self.properties['level']} and apoptosis rate {self.properties['apoptosis_rate']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        dusp4_high = DUSP4("DUSP4_high", level=5)  # High DUSP4 level
        dusp4_low = DUSP4("DUSP4_low", level=1)    # Low DUSP4 level
        world.addObject(dusp4_high)
        world.addObject(dusp4_low)
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

        # Do one tick of the environment
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

    # Check the apoptosis rates to verify the claim
    dusp4_high = simulation.rootObject.containsItemWithName("DUSP4_high")[0]
    dusp4_low = simulation.rootObject.containsItemWithName("DUSP4_low")[0]

    if dusp4_high.properties["apoptosis_rate"] > dusp4_low.properties["apoptosis_rate"]:
        print("Claim Supported: DUSP4 increases apoptosis.")
    else:
        print("Claim Refuted: DUSP4 does not increase apoptosis.")

if __name__ == "__main__":
    main()
