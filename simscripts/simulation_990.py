
# Claim: Pyridostatin decreases telomere fragility in BRCA2-deficient cells.
# The simulation will test the effect of Pyridostatin on telomere fragility in BRCA2-deficient cells.

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
    def __init__(self, name, brca2_deficient=False):
        super().__init__(name)
        self.properties = {
            "brca2_deficient": brca2_deficient,
            "telomere_fragility": 0  # 0 means stable, higher means more fragile
        }

    def apply_pyridostatin(self):
        if self.properties["brca2_deficient"]:
            self.properties["telomere_fragility"] += 1  # Increase fragility when treated with Pyridostatin

    def makeDescriptionStr(self):
        description = f"A {self.name} cell, BRCA2 deficient: {self.properties['brca2_deficient']}, Telomere fragility level: {self.properties['telomere_fragility']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell_environment")
        brca2_deficient_cell = Cell("BRCA2-deficient cell", brca2_deficient=True)
        world.addObject(brca2_deficient_cell)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("apply pyridostatin", ["apply_pyridostatin"])

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

        if actionVerb == "apply_pyridostatin":
            cell = self.rootObject.contains[0]  # Get the BRCA2-deficient cell
            cell.apply_pyridostatin()
            self.observationStr = f"Pyridostatin applied to {cell.name}."
        
        # Update the description after the action
        self.observationStr += "\n" + self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "apply pyridostatin"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
