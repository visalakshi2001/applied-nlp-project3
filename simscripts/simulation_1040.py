
# Claim: Replacement of histone H2A with H2A.Z accelerates gene activation in yeasts by destabilizing +1 nucleosomes.
# The simulation will model nucleosome stability with H2A and H2A.Z variants.

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

class Nucleosome(GameObject):
    def __init__(self, name, stability):
        super().__init__(name)
        self.properties["stability"] = stability  # Stability of the nucleosome

    def tick(self):
        # Simulate the effect of H2A.Z on stability
        if "H2A.Z" in self.name:
            self.properties["stability"] -= 1  # H2A.Z destabilizes the nucleosome
        else:
            self.properties["stability"] += 1  # H2A stabilizes the nucleosome

    def makeDescriptionStr(self):
        return f"{self.name} with stability level: {self.properties['stability']}"

class World(Container):
    def __init__(self):
        super().__init__("nucleosome environment")

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
        nucleosome_H2A = Nucleosome("Nucleosome with H2A", stability=5)
        nucleosome_H2A_Z = Nucleosome("Nucleosome with H2A.Z", stability=5)
        world.addObject(nucleosome_H2A)
        world.addObject(nucleosome_H2A_Z)
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
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The output of the simulation will show the stability of nucleosomes with H2A and H2A.Z.
# If H2A.Z nucleosome has lower stability than H2A, it supports the claim.
