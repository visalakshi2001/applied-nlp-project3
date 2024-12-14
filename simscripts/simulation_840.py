
# Claim: Natriuretic peptides increase susceptibility to diabetes.
# The simulation will analyze the relationship between NT-pro-BNP levels and the risk of type 2 diabetes (T2D).

from simulation_utils import GameObject, Container

class NatriureticPeptide(GameObject):
    def __init__(self, name, level):
        super().__init__(name)
        self.properties = {
            "level": level,  # NT-pro-BNP level
            "risk_of_T2D": 0  # Risk of type 2 diabetes
        }

    def tick(self):
        # The risk of T2D decreases with higher NT-pro-BNP levels
        self.properties["risk_of_T2D"] = max(0, 1 - (self.properties["level"] / 10))  # Arbitrary scaling

    def makeDescriptionStr(self):
        return f"{self.name} with NT-pro-BNP level {self.properties['level']} has a risk of T2D: {self.properties['risk_of_T2D']:.2f}"

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
        natriuretic_peptide_low = NatriureticPeptide("Low NT-pro-BNP", 2)  # Low level
        natriuretic_peptide_high = NatriureticPeptide("High NT-pro-BNP", 8)  # High level
        world.addObject(natriuretic_peptide_low)
        world.addObject(natriuretic_peptide_high)
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

    # Analyze the results to determine if the claim is supported or refuted
    low_risk = simulation.rootObject.contains[0].properties["risk_of_T2D"]
    high_risk = simulation.rootObject.contains[1].properties["risk_of_T2D"]

    if high_risk < low_risk:
        print("Claim Supported: Higher NT-pro-BNP levels are associated with lower risk of T2D.")
    else:
        print("Claim Refuted: Higher NT-pro-BNP levels do not increase susceptibility to diabetes.")

if __name__ == "__main__":
    main()
