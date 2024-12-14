
# The Snf1 complex regulates carbon and energy metabolism in baker's yeast (Saccharomyces cerevisiae).

from simulation_utils import GameObject, Container

class Yeast(GameObject):
    def __init__(self, name, snf1_activity=0, energy_metabolism=0):
        super().__init__(name)
        self.properties = {
            "snf1_activity": snf1_activity,
            "energy_metabolism": energy_metabolism
        }

    def tick(self):
        # Simulate the effect of Snf1 activity on energy metabolism
        self.properties["energy_metabolism"] = self.properties["snf1_activity"] * 2  # Arbitrary multiplier for simulation

    def makeDescriptionStr(self):
        description = f"A {self.name}, with Snf1 activity level at {self.properties['snf1_activity']} and energy metabolism at {self.properties['energy_metabolism']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        yeast = Yeast("baker's yeast")
        world.addObject(yeast)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"increase Snf1 activity of {objReferent}", ["increase", obj])
                self.addAction(f"decrease Snf1 activity of {objReferent}", ["decrease", obj])

    def actionIncrease(self, yeast):
        if type(yeast) != Yeast:
            return f"Cannot increase the Snf1 activity of {yeast.name}."
        else:
            yeast.properties["snf1_activity"] += 1
            return f"You increase the Snf1 activity of {yeast.name} by 1."
        
    def actionDecrease(self, yeast):
        if type(yeast) != Yeast:
            return f"Cannot decrease the Snf1 activity of {yeast.name}."
        else:
            yeast.properties["snf1_activity"] -= 1
            return f"You decrease the Snf1 activity of {yeast.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            self.observationStr = self.actionIncrease(action[1])
        elif actionVerb == "decrease":
            self.observationStr = self.actionDecrease(action[1])

        self.doWorldTick()
        self.generatePossibleActions()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase Snf1 activity of baker's yeast", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the final state to determine if the claim is supported or refuted
    yeast = simulation.rootObject.containsItemWithName("baker's yeast")[0]
    if yeast.properties["energy_metabolism"] > 0:
        print("Claim Supported: The Snf1 complex regulates carbon and energy metabolism in baker's yeast.")
    else:
        print("Claim Refuted: The Snf1 complex does not regulate carbon and energy metabolism in baker's yeast.")

if __name__ == "__main__":
    main()
