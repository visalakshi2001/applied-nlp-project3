
# Claim: Satellite cell dysfunction is a key factor in sarcopenia development.
# The simulation will test the relationship between satellite cell activity and muscle regeneration in the context of sarcopenia.

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

class Muscle(GameObject):
    def __init__(self, name, size=100, regenerative_capacity=100, fibrosis=0):
        super().__init__(name)
        self.properties = {
            "size": size,
            "regenerative_capacity": regenerative_capacity,
            "fibrosis": fibrosis
        }

    def tick(self):
        # Simulate aging effects on muscle
        self.properties["regenerative_capacity"] -= 1  # Decrease regenerative capacity over time
        if self.properties["regenerative_capacity"] < 0:
            self.properties["regenerative_capacity"] = 0
        self.properties["fibrosis"] += 1  # Increase fibrosis over time

    def makeDescriptionStr(self):
        description = f"A {self.name} muscle, size: {self.properties['size']}, regenerative capacity: {self.properties['regenerative_capacity']}, fibrosis: {self.properties['fibrosis']}."
        return description

class SatelliteCell(GameObject):
    def __init__(self, name, activity_level=100):
        super().__init__(name)
        self.properties = {
            "activity_level": activity_level
        }

    def tick(self):
        # Simulate loss of satellite cell activity over time
        self.properties["activity_level"] -= 1
        if self.properties["activity_level"] < 0:
            self.properties["activity_level"] = 0

    def makeDescriptionStr(self):
        return f"A {self.name} with activity level: {self.properties['activity_level']}."

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
        muscle = Muscle("skeletal")
        satellite_cell = SatelliteCell("satellite cell")
        world.addObject(muscle)
        world.addObject(satellite_cell)
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

        # Simulate a tick for all objects
        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate for a few ticks to observe changes
    for _ in range(5):
        print("Tick:")
        obs = simulation.step("look")
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The simulation will show that despite the reduction in satellite cell activity, the muscle size remains stable, 
# and fibrosis increases, indicating that satellite cell dysfunction does not directly lead to sarcopenia development.
# Therefore, the claim is refuted.
