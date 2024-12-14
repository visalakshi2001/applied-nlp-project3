
# Claim: Monoclonal antibody targeting of N-cadherin encourages castration resistance.
# The simulation will model the effects of N-cadherin targeting on castration resistance in prostate cancer.

from simulation_utils import GameObject, Container

class NCadherin(GameObject):
    def __init__(self, name, expression_level=0):
        super().__init__(name)
        self.properties = {
            "expression_level": expression_level,  # Level of N-cadherin expression
            "castration_resistance": False  # Indicates if castration resistance has emerged
        }

    def tick(self):
        # Simulate the effect of N-cadherin expression on castration resistance
        if self.properties["expression_level"] > 5:  # Arbitrary threshold for resistance
            self.properties["castration_resistance"] = True

    def makeDescriptionStr(self):
        return f"{self.name} with expression level {self.properties['expression_level']} and castration resistance status: {self.properties['castration_resistance']}."

class MonoclonalAntibody(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def target(self, n_cadherin):
        # Simulate the effect of monoclonal antibody targeting N-cadherin
        n_cadherin.properties["expression_level"] -= 3  # Decrease expression level
        if n_cadherin.properties["expression_level"] < 0:
            n_cadherin.properties["expression_level"] = 0  # Prevent negative expression

class ProstateCancerModel(Container):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = ProstateCancerModel("Prostate Cancer Environment")
        n_cadherin = NCadherin("N-cadherin", expression_level=8)  # Initial high expression
        antibody = MonoclonalAntibody("N-cadherin Monoclonal Antibody")
        world.addObject(n_cadherin)
        world.addObject(antibody)
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
        self.addAction("target N-cadherin", ["target", allObjects["N-cadherin"][0]])

    def actionTarget(self, antibody, n_cadherin):
        if isinstance(antibody, MonoclonalAntibody) and isinstance(n_cadherin, NCadherin):
            antibody.target(n_cadherin)
            return f"{antibody.name} targeted {n_cadherin.name}."
        return "Invalid action."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "target":
            self.observationStr = self.actionTarget(action[1], self.rootObject.containsItemWithName("N-cadherin")[0])

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "target N-cadherin"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check on N-cadherin's castration resistance status
    n_cadherin = simulation.rootObject.containsItemWithName("N-cadherin")[0]
    if n_cadherin.properties["castration_resistance"]:
        print("Claim Refuted: Monoclonal antibody targeting did not prevent castration resistance.")
    else:
        print("Claim Supported: Monoclonal antibody targeting delayed emergence of castration resistance.")

if __name__ == "__main__":
    main()
