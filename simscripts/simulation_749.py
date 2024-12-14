
# Claim: Major antigen-induced signals from the T cell receptor and secondary signals from costimulatory receptors are required for T cell activation.
# The simulation will demonstrate the importance of TCR and CD28 signals in T cell activation.

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

class TCell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "TCR_signal": 0,
            "CD28_signal": 0,
            "activated": False
        }

    def activate(self):
        if self.properties["TCR_signal"] > 0 and self.properties["CD28_signal"] > 0:
            self.properties["activated"] = True

    def tick(self):
        self.activate()

    def makeDescriptionStr(self):
        activation_status = "activated" if self.properties["activated"] else "not activated"
        return f"A T cell named {self.name} is {activation_status}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("immune system")
        t_cell = TCell("T_Cell_1")
        world.addObject(t_cell)
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
                self.addAction(f"signal TCR for {objReferent}", ["signal_TCR", obj])
                self.addAction(f"signal CD28 for {objReferent}", ["signal_CD28", obj])

    def actionSignalTCR(self, t_cell):
        if type(t_cell) != TCell:
            return f"Cannot signal TCR for {t_cell.name}."
        else:
            t_cell.properties["TCR_signal"] += 1
            return f"You signal TCR for {t_cell.name}."

    def actionSignalCD28(self, t_cell):
        if type(t_cell) != TCell:
            return f"Cannot signal CD28 for {t_cell.name}."
        else:
            t_cell.properties["CD28_signal"] += 1
            return f"You signal CD28 for {t_cell.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "signal_TCR"):
            self.observationStr = self.actionSignalTCR(action[1])
        elif (actionVerb == "signal_CD28"):
            self.observationStr = self.actionSignalCD28(action[1])

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
    actions = ["signal TCR for T_Cell_1", "signal CD28 for T_Cell_1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
