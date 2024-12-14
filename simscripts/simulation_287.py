
# Claim: Converting apoE4 to apoE3 by gene editing worsens the pathology associated with apoE4 in human iPSCderived neurons.
# The simulation will test the effects of converting apoE4 to apoE3 on neuronal pathology.

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
    def __init__(self, name, apoE_type):
        super().__init__(name)
        self.apoE_type = apoE_type
        self.properties = {
            "tau_phosphorylation": 0,
            "Aβ_production": 0,
            "GABAergic_degeneration": False
        }

    def tick(self):
        if self.apoE_type == "ApoE4":
            self.properties["tau_phosphorylation"] += 1
            self.properties["Aβ_production"] += 2
            self.properties["GABAergic_degeneration"] = True
        elif self.apoE_type == "ApoE3":
            self.properties["tau_phosphorylation"] -= 1
            self.properties["Aβ_production"] -= 1
            self.properties["GABAergic_degeneration"] = False

    def makeDescriptionStr(self):
        description = f"{self.name} (Type: {self.apoE_type}) - Tau Phosphorylation: {self.properties['tau_phosphorylation']}, Aβ Production: {self.properties['Aβ_production']}, GABAergic Degeneration: {self.properties['GABAergic_degeneration']}."
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
        apoE4_neuron = Neuron("ApoE4 Neuron", "ApoE4")
        apoE3_neuron = Neuron("ApoE3 Neuron", "ApoE3")
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

    # Simulate the conversion of ApoE4 to ApoE3
    print("Converting ApoE4 to ApoE3...")
    apoE4_neuron = simulation.rootObject.containsItemWithName("ApoE4 Neuron")[0]
    apoE3_neuron = simulation.rootObject.containsItemWithName("ApoE3 Neuron")[0]

    # Before conversion
    print("Before conversion:")
    print(simulation.rootObject.makeDescriptionStr())

    # Simulate the conversion
    apoE4_neuron.apoE_type = "ApoE3"
    apoE4_neuron.properties["tau_phosphorylation"] = 0
    apoE4_neuron.properties["Aβ_production"] = 0
    apoE4_neuron.properties["GABAergic_degeneration"] = False

    # After conversion
    print("After conversion:")
    print(simulation.rootObject.makeDescriptionStr())

if __name__ == "__main__":
    main()
