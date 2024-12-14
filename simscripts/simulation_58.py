
# Claim: APOE4 expression in iPSC-derived neurons results in decreased tau phosphorylation.
# The simulation will test the relationship between APOE4 expression and tau phosphorylation levels.

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
    def __init__(self, name, tau_phosphorylation=0, APOE_expression="APOE3"):
        super().__init__(name)
        self.properties = {
            "tau_phosphorylation": tau_phosphorylation,
            "APOE_expression": APOE_expression
        }

    def tick(self):
        if self.properties["APOE_expression"] == "APOE4":
            self.properties["tau_phosphorylation"] += 1  # Increase tau phosphorylation for APOE4
        elif self.properties["APOE_expression"] == "APOE3":
            self.properties["tau_phosphorylation"] -= 1  # Decrease tau phosphorylation for APOE3

    def makeDescriptionStr(self):
        description = f"A {self.name} neuron with {self.properties['APOE_expression']} expression, tau phosphorylation level is {self.properties['tau_phosphorylation']}."
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
        apoE4_neuron = Neuron("APOE4 Neuron", tau_phosphorylation=0, APOE_expression="APOE4")
        apoE3_neuron = Neuron("APOE3 Neuron", tau_phosphorylation=0, APOE_expression="APOE3")
        world.addObject(apoE4_neuron)
        world.addObject(apoE3_neuron)        
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
    
    # Perform a tick to simulate the effect of APOE4 expression
    simulation.step("look")
    print("After one tick:")
    print(simulation.observationStr)

    # Check the tau phosphorylation levels
    apoE4_neuron = simulation.rootObject.containsItemWithName("APOE4 Neuron")[0]
    apoE3_neuron = simulation.rootObject.containsItemWithName("APOE3 Neuron")[0]

    if apoE4_neuron.properties["tau_phosphorylation"] > apoE3_neuron.properties["tau_phosphorylation"]:
        result = "Refuted"
    else:
        result = "Supported"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
