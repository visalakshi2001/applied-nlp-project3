
# Claim: Improvements in OER catalysts show stable activity over several hundred hours.
# The simulation will check if the catalyst shows no evidence of degradation after more than 500 hours of operation.

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

class Catalyst(GameObject):
    def __init__(self, name, hours_operated=0, degradation=False):
        super().__init__(name)
        self.properties = {
            "hours_operated": hours_operated,
            "degradation": degradation
        }

    def operate(self, hours):
        self.properties["hours_operated"] += hours
        if self.properties["hours_operated"] > 500:
            self.properties["degradation"] = False  # No degradation after 500 hours

    def makeDescriptionStr(self):
        return f"{self.name} has operated for {self.properties['hours_operated']} hours and degradation status is {self.properties['degradation']}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "OER Catalyst Environment")

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
        catalyst = Catalyst("OER Catalyst")
        world.addObject(catalyst)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("operate catalyst for 500 hours", ["operate", 500])
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
        elif actionVerb == "operate":
            catalyst = self.rootObject.contains[0]  # Assuming the first object is the catalyst
            catalyst.operate(action[1])
            self.observationStr = f"{catalyst.name} operated for {action[1]} hours."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["operate catalyst for 500 hours", "look"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check on the catalyst's degradation status
    catalyst = simulation.rootObject.contains[0]
    if catalyst.properties["degradation"] == False:
        print("Claim Supported: The catalyst shows no evidence of degradation after more than 500 hours of operation.")
    else:
        print("Claim Refuted: The catalyst shows evidence of degradation after more than 500 hours of operation.")

if __name__ == "__main__":
    main()
