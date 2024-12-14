
# Claim: Pyridostatin stabilizes the G - quadruplex in the telomeric region.
# The simulation will test the effects of pyridostatin on telomere stability.

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

class Telomere(GameObject):
    def __init__(self, name, stability=100):
        super().__init__(name)
        self.properties = {
            "stability": stability
        }

    def applyPyridostatin(self):
        # Pyridostatin is supposed to stabilize G-quadruplex, but in this case, it increases instability
        self.properties["stability"] -= 20  # Decrease stability to simulate fragility

    def tick(self):
        # Simulate the effect of time on telomere stability
        self.properties["stability"] -= 1  # Natural degradation over time

    def makeDescriptionStr(self):
        return f"A telomere named {self.name} with stability level: {self.properties['stability']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        telomere = Telomere("telomere_1")
        world.addObject(telomere)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("apply pyridostatin", ["apply", self.rootObject.contains[0]])

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

        if actionVerb == "apply":
            action[1].applyPyridostatin()
            self.observationStr = f"{action[1].name} has been treated with pyridostatin."
        
        # Do one tick of the environment
        self.doWorldTick()
        return self.observationStr + "\n" + self.rootObject.makeDescriptionStr()

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "apply pyridostatin"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
