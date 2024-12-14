
# Claim: Notch signaling occurs between tumor cells and stromal cells.
# The simulation will model tumor cells and stromal cells to observe interactions related to Notch signaling.

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
    def __init__(self, name, is_tumor=False):
        super().__init__(name)
        self.properties = {
            "is_tumor": is_tumor,
            "Notch_signaling": False
        }

    def activateNotchSignaling(self):
        self.properties["Notch_signaling"] = True

    def makeDescriptionStr(self):
        cell_type = "tumor" if self.properties["is_tumor"] else "stromal"
        return f"A {cell_type} cell named {self.name}, Notch signaling is {'active' if self.properties['Notch_signaling'] else 'inactive'}."

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
        tumor_cell = Cell("Tumor Cell 1", is_tumor=True)
        stromal_cell = Cell("Stromal Cell 1", is_tumor=False)
        world.addObject(tumor_cell)
        world.addObject(stromal_cell)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}

        self.addAction("look", ["look"])
        self.addAction("activate Notch signaling in Tumor Cell 1", ["activate", "Tumor Cell 1"])
        self.addAction("activate Notch signaling in Stromal Cell 1", ["activate", "Stromal Cell 1"])

    def actionActivateNotch(self, cell_name):
        cell = self.rootObject.containsItemWithName(cell_name)
        if cell:
            cell[0].activateNotchSignaling()
            return f"Notch signaling activated in {cell_name}."
        return f"{cell_name} not found."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "activate":
            self.observationStr = self.actionActivateNotch(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "activate Notch signaling in Tumor Cell 1", "look", "activate Notch signaling in Stromal Cell 1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
