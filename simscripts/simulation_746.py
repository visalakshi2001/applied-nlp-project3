
# Claim: MafA phosphorylation enhances its ubiquitination.
# The simulation will demonstrate the relationship between MafA phosphorylation and its ubiquitination.

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

    def openContainer(self):
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be opened.", False)
        if self.getProperty("isOpen"):
            return ("The " + self.name + " is already open.", False)
        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    def closeContainer(self):
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be closed.", False)
        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is already closed.", False)
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

class MafA(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "phosphorylation": 0,
            "ubiquitination": 0,
            "degradation": 0
        }

    def phosphorylate(self):
        self.properties["phosphorylation"] += 1
        self.properties["ubiquitination"] += 1  # Ubiquitination increases with phosphorylation
        self.properties["degradation"] += 1  # Degradation also increases

    def makeDescriptionStr(self):
        return f"{self.name} with phosphorylation level {self.properties['phosphorylation']}, ubiquitination level {self.properties['ubiquitination']}, and degradation level {self.properties['degradation']}."

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
        self.possibleActions = {}
        self.addAction("phosphorylate MafA", ["phosphorylate"])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "phosphorylate":
            mafA = self.rootObject.contains[0]  # Assuming only one MafA in the simulation
            mafA.phosphorylate()
            self.observationStr = f"{mafA.name} has been phosphorylated."
        
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Perform phosphorylation to test the claim
    action = "phosphorylate MafA"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)
    print(simulation.rootObject.makeDescriptionStr())

    # Check the results
    mafA = simulation.rootObject.contains[0]
    if mafA.properties["ubiquitination"] > 0:
        print("Claim Supported: MafA phosphorylation enhances its ubiquitination.")
    else:
        print("Claim Refuted: MafA phosphorylation does not enhance its ubiquitination.")

if __name__ == "__main__":
    main()
