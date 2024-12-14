
# Claim: Removal of H3K9me3 by ectopic expression of other H3K9 demethylases decreases reprogramming efficiency in SCNT experiments.
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

class H3K9Demethylase(GameObject):
    def __init__(self, name, efficiency=0):
        super().__init__(name)
        self.properties = {
            "efficiency": efficiency
        }

    def tick(self):
        # Simulate the effect of demethylase on reprogramming efficiency
        if self.getProperty("efficiency") < 1:
            self.properties["efficiency"] += 0.1  # Increase efficiency slightly

    def makeDescriptionStr(self):
        return f"{self.name} with reprogramming efficiency of {self.properties['efficiency']}."

class SCNTExperiment(Container):
    def __init__(self):
        super().__init__("SCNT Experiment")
        self.demethylases = []

    def addDemethylase(self, demethylase):
        self.addObject(demethylase)
        self.demethylases.append(demethylase)

    def calculateEfficiency(self):
        total_efficiency = sum(demethylase.getProperty("efficiency") for demethylase in self.demethylases)
        return total_efficiency / len(self.demethylases) if self.demethylases else 0

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("World")
        scnt_experiment = SCNTExperiment()
        kdm4e = H3K9Demethylase("KDM4E", efficiency=0.5)
        kdm4d = H3K9Demethylase("KDM4D", efficiency=0.3)
        scnt_experiment.addDemethylase(kdm4e)
        scnt_experiment.addDemethylase(kdm4d)
        world.addObject(scnt_experiment)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "tick": ["tick"]
        }

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
            for obj in self.rootObject.getAllContainedObjectsRecursive():
                obj.tick()
            efficiency = self.rootObject.contains[0].calculateEfficiency()
            self.observationStr = f"Current reprogramming efficiency: {efficiency}."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "tick", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
