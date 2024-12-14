
# Claim: Forkhead 0 (fox0) transcription factors are involved in cellular differentiation.
# The simulation will demonstrate the role of Forkhead O (FoxO) transcription factors in cellular differentiation.

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

class ForkheadO(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "involved_in_differentiation": True,
            "cell_cycle_arrest": True,
            "stress_resistance": True,
            "apoptosis": True,
            "metabolism": True
        }

    def makeDescriptionStr(self):
        description = f"{self.name} is a Forkhead O transcription factor involved in cellular differentiation."
        return description

class StemCell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_differentiated": False
        }

    def differentiate(self):
        self.properties["is_differentiated"] = True

    def makeDescriptionStr(self):
        state = "differentiated" if self.properties["is_differentiated"] else "undifferentiated"
        return f"{self.name} is a stem cell and is currently {state}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "cellular environment")

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
        foxO = ForkheadO("FoxO1")
        stemCell = StemCell("Hematopoietic Stem Cell")
        world.addObject(foxO)
        world.addObject(stemCell)
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
        self.addAction("differentiate Hematopoietic Stem Cell", ["differentiate", allObjects["Hematopoietic Stem Cell"][0]])

    def actionDifferentiate(self, stemCell):
        if type(stemCell) != StemCell:
            return f"Cannot differentiate {stemCell.name}."
        else:
            stemCell.differentiate()
            return f"{stemCell.name} has differentiated."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "differentiate"):
            self.observationStr = self.actionDifferentiate(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "differentiate Hematopoietic Stem Cell"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
