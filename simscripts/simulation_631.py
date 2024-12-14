
# Claim: Inhibiting HDAC6 increases survival of mice with ARID1A mutated tumors.
# This simulation will model the effect of HDAC6 inhibition on the survival of mice with ARID1A mutated tumors.

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

class Mouse(GameObject):
    def __init__(self, name, survival_rate=100):
        super().__init__(name)
        self.properties = {
            "survival_rate": survival_rate,
            "is_inhibited": False
        }

    def inhibitHDAC6(self):
        self.properties["is_inhibited"] = True
        self.properties["survival_rate"] += 20  # Inhibition increases survival rate

    def makeDescriptionStr(self):
        return f"{self.name} with survival rate: {self.properties['survival_rate']}% and HDAC6 inhibition status: {self.properties['is_inhibited']}."

class Tumor(GameObject):
    def __init__(self, name, is_arid1a_mutated=False):
        super().__init__(name)
        self.properties = {
            "is_arid1a_mutated": is_arid1a_mutated
        }

    def makeDescriptionStr(self):
        return f"{self.name} is ARID1A mutated: {self.properties['is_arid1a_mutated']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        mouse = Mouse("Mouse_1")
        tumor = Tumor("Tumor_1", is_arid1a_mutated=True)
        world.addObject(mouse)
        world.addObject(tumor)
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
        self.addAction("inhibit HDAC6", ["inhibit", allObjects["Mouse_1"][0]])

    def actionInhibitHDAC6(self, mouse):
        if type(mouse) != Mouse:
            return f"Cannot inhibit HDAC6 of {mouse.name}."
        else:
            mouse.inhibitHDAC6()
            return f"You inhibit HDAC6 of {mouse.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "inhibit"):
            self.observationStr = self.actionInhibitHDAC6(action[1])
        
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "inhibit HDAC6"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
