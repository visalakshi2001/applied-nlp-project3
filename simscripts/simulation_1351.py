
# Claim: Upregulation of dynein in Drosophila neurons increases the number of microtubule plus-ends growing toward the cell body of each neuron.
# The simulation will model the effect of dynein on microtubule orientation in Drosophila neurons.

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

class Neuron(GameObject):
    def __init__(self, name, dynein_level=0):
        super().__init__(name)
        self.properties = {
            "dynein_level": dynein_level,
            "microtubule_plus_ends": 0
        }

    def tick(self):
        # Increase the number of microtubule plus-ends based on dynein level
        self.properties["microtubule_plus_ends"] = self.properties["dynein_level"] * 5  # Arbitrary multiplier for simulation

    def makeDescriptionStr(self):
        description = f"A {self.name} neuron with dynein level {self.properties['dynein_level']} and {self.properties['microtubule_plus_ends']} microtubule plus-ends."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "Drosophila Neuron Environment")

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
        neuron = Neuron("Drosophila Neuron", dynein_level=2)  # Upregulating dynein
        world.addObject(neuron)        
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
    print("After one tick:")
    simulation.step("look")
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
