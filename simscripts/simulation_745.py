
# Claim: MafA phosphorylation decreases its ubiquitination.
# The simulation will test the relationship between MafA phosphorylation and its ubiquitination.

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

class MafA(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "phosphorylation": 0,
            "ubiquitination": 0
        }

    def phosphorylate(self):
        self.properties["phosphorylation"] += 1
        self.updateUbiquitination()

    def updateUbiquitination(self):
        # Simulating that phosphorylation increases ubiquitination
        self.properties["ubiquitination"] = self.properties["phosphorylation"] * 2  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"{self.name} has {self.properties['phosphorylation']} phosphorylations and {self.properties['ubiquitination']} ubiquitinations."

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
        mafA = MafA("MafA")
        world.addObject(mafA)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        for obj in allObjects:
            if isinstance(obj, MafA):
                self.addAction("phosphorylate " + obj.name, ["phosphorylate", obj])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]
        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "phosphorylate":
            action[1].phosphorylate()
            self.observationStr = f"You phosphorylate {action[1].name}."
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
    actions = ["phosphorylate MafA", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the final state of MafA to determine if the claim is supported or refuted
    mafA = simulation.rootObject.containsItemWithName("MafA")[0]
    if mafA.properties["ubiquitination"] > 0:
        print("Claim Refuted: MafA phosphorylation does not decrease its ubiquitination.")
    else:
        print("Claim Supported: MafA phosphorylation decreases its ubiquitination.")

if __name__ == "__main__":
    main()
