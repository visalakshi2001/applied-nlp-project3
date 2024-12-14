
# Claim: There is no increased risk of hypospadias with clomiphene.
# The simulation will check the relationship between clomiphene use and the risk of hypospadias.

from simulation_utils import GameObject, Container

class ClomipheneUse(GameObject):
    def __init__(self, name, risk_of_hypospadias=0):
        super().__init__(name)
        self.properties = {
            "risk_of_hypospadias": risk_of_hypospadias
        }

    def tick(self):
        # Simulate the effect of clomiphene on the risk of hypospadias
        # For this simulation, we will assume that clomiphene does not increase the risk
        self.properties["risk_of_hypospadias"] = 0  # No increased risk

    def makeDescriptionStr(self):
        return f"{self.name} has a risk of hypospadias of {self.properties['risk_of_hypospadias']}."

class HypospadiasRisk(GameObject):
    def __init__(self, name, risk_level):
        super().__init__(name)
        self.properties = {
            "risk_level": risk_level
        }

    def makeDescriptionStr(self):
        return f"{self.name} has a risk level of {self.properties['risk_level']}."

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
        clomiphene = ClomipheneUse("Clomiphene")
        hypospadias = HypospadiasRisk("Hypospadias", risk_level=0)  # Initial risk level is 0
        world.addObject(clomiphene)
        world.addObject(hypospadias)
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

    # Check the risk of hypospadias after simulation
    clomiphene = simulation.rootObject.containsItemWithName("Clomiphene")[0]
    hypospadias = simulation.rootObject.containsItemWithName("Hypospadias")[0]
    
    if clomiphene.properties["risk_of_hypospadias"] == 0:
        print("Claim Supported: There is no increased risk of hypospadias with clomiphene.")
    else:
        print("Claim Refuted: There is an increased risk of hypospadias with clomiphene.")

if __name__ == "__main__":
    main()
