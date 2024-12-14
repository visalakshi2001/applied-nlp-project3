
# Claim: Lack of FGF21 in mice leads to atherosclerotic plaque formation.
# The simulation will model the effects of FGF21 deficiency on atherosclerotic plaque formation in mice.

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

class Mouse(GameObject):
    def __init__(self, name, FGF21_level=0, plaque_formation=0):
        super().__init__(name)
        self.properties = {
            "FGF21_level": FGF21_level,
            "plaque_formation": plaque_formation
        }

    def tick(self):
        # If FGF21 is deficient (0), increase plaque formation
        if self.properties["FGF21_level"] == 0:
            self.properties["plaque_formation"] += 1  # Simulate plaque formation increase

    def makeDescriptionStr(self):
        description = f"A {self.name} with FGF21 level {self.properties['FGF21_level']} and plaque formation level {self.properties['plaque_formation']}."
        return description

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
        mouse_with_FGF21 = Mouse("Mouse with FGF21", FGF21_level=1)
        mouse_without_FGF21 = Mouse("Mouse without FGF21", FGF21_level=0)
        world.addObject(mouse_with_FGF21)
        world.addObject(mouse_without_FGF21)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            # Perform a tick to simulate time passing
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate multiple ticks to observe plaque formation
    for _ in range(5):
        print("Ticking...")
        obs = simulation.step("tick")
        print(obs)

if __name__ == "__main__":
    main()
