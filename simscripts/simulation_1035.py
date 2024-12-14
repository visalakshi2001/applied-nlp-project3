
# Claim: Removal of H3K9me3 by ectopic expression of other H3K9 demethylases improves reprogramming efficiency in SCNT experiments.
# The simulation will model the effect of H3K9 demethylases on SCNT reprogramming efficiency.

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

class Demethylase(GameObject):
    def __init__(self, name, efficiency=0):
        super().__init__(name)
        self.properties = {
            "efficiency": efficiency
        }

    def tick(self):
        # Simulate the effect of demethylase on reprogramming efficiency
        self.properties["efficiency"] += 1  # Each tick represents an improvement in efficiency

    def makeDescriptionStr(self):
        return f"{self.name} with current efficiency: {self.properties['efficiency']}"

class SCNTExperiment(Container):
    def __init__(self):
        super().__init__("SCNT Experiment")
        self.properties["reprogramming_efficiency"] = 0

    def tick(self):
        # Update the reprogramming efficiency based on contained demethylases
        for demethylase in self.contains:
            self.properties["reprogramming_efficiency"] += demethylase.getProperty("efficiency")

    def makeDescriptionStr(self):
        return f"In the {self.name}, the current reprogramming efficiency is: {self.properties['reprogramming_efficiency']}"

class World(Container):
    def __init__(self):
        super().__init__("environment")

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
        scnt_experiment = SCNTExperiment()
        demethylase1 = Demethylase("KDM4D")
        demethylase2 = Demethylase("KDM4E")
        scnt_experiment.addObject(demethylase1)
        scnt_experiment.addObject(demethylase2)
        world.addObject(scnt_experiment)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

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

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Do one tick of the environment
        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    for _ in range(5):  # Simulate 5 ticks to see the improvement
        obs = simulation.step("look")
        print(obs)
        print()

if __name__ == "__main__":
    main()
