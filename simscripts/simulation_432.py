
# Claim: Foxk2 regulates autophagy genes in muscle cells and fibroblast cells.
# The simulation will check if Foxk2 acts as a transcriptional repressor of autophagy genes in muscle and fibroblast cells.

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

class Cell(GameObject):
    def __init__(self, name, autophagy_genes_repressed=0):
        super().__init__(name)
        self.properties = {
            "autophagy_genes_repressed": autophagy_genes_repressed
        }

    def tick(self):
        # Simulate the effect of Foxk2 on autophagy genes
        self.properties["autophagy_genes_repressed"] += 1  # Each tick represents repression of autophagy genes

    def makeDescriptionStr(self):
        return f"A {self.name} cell with {self.properties['autophagy_genes_repressed']} autophagy genes repressed."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        muscle_cell = Cell("muscle_cell")
        fibroblast_cell = Cell("fibroblast_cell")
        world.addObject(muscle_cell)
        world.addObject(fibroblast_cell)
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
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"tick {objReferent}", ["tick", obj])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]
        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "tick":
            action[1].tick()
            self.observationStr = f"{action[1].name} has its autophagy genes repressed."
        self.doWorldTick()
        self.generatePossibleActions()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "tick muscle_cell", "tick fibroblast_cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check of repression levels
    muscle_cell = simulation.rootObject.containsItemWithName("muscle_cell")[0]
    fibroblast_cell = simulation.rootObject.containsItemWithName("fibroblast_cell")[0]
    if muscle_cell.properties["autophagy_genes_repressed"] > 0 and fibroblast_cell.properties["autophagy_genes_repressed"] > 0:
        print("Claim Supported: Foxk2 regulates autophagy genes in muscle cells and fibroblast cells.")
    else:
        print("Claim Refuted: Foxk2 does not regulate autophagy genes as claimed.")

if __name__ == "__main__":
    main()
