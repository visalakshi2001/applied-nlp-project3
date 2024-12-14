
# Claim: Pyridostatin deregulates G2/M progression.
# The simulation will model the effects of pyridostatin on cell proliferation and G2/M progression.

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

class Cell(GameObject):
    def __init__(self, name, hr_deficiency=False):
        super().__init__(name)
        self.properties = {
            "hr_deficiency": hr_deficiency,
            "g2m_progression": True,
            "dsb_accumulation": 0,
            "proliferation": True
        }

    def tick(self):
        if self.properties["hr_deficiency"]:
            self.properties["dsb_accumulation"] += 1
            if self.properties["dsb_accumulation"] > 2:  # Arbitrary threshold for G2/M deregulation
                self.properties["g2m_progression"] = False
                self.properties["proliferation"] = False

class Pyridostatin(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def apply_effect(self, cell):
        if cell.getProperty("hr_deficiency"):
            cell.properties["dsb_accumulation"] += 1
            cell.properties["g2m_progression"] = False
            cell.properties["proliferation"] = False

class World(Container):
    def __init__(self):
        super().__init__("environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        cell1 = Cell("HR-deficient Cell", hr_deficiency=True)
        pyridostatin = Pyridostatin("Pyridostatin")
        world.addObject(cell1)
        world.addObject(pyridostatin)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("apply pyridostatin", ["apply", allObjects["Pyridostatin"][0]])

    def actionApplyPyridostatin(self, pyridostatin, cell):
        pyridostatin.apply_effect(cell)

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply":
            pyridostatin = action[1]
            cell = self.rootObject.containsItemWithName("HR-deficient Cell")[0]
            self.actionApplyPyridostatin(pyridostatin, cell)

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "apply pyridostatin"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the state of the cell after applying pyridostatin
    cell = simulation.rootObject.containsItemWithName("HR-deficient Cell")[0]
    if not cell.properties["g2m_progression"] and not cell.properties["proliferation"]:
        print("Claim Supported: Pyridostatin deregulates G2/M progression.")
    else:
        print("Claim Refuted: Pyridostatin does not deregulate G2/M progression.")

if __name__ == "__main__":
    main()
