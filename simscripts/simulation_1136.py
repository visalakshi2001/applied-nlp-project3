
# Claim: TNFAIP3 is a tumor enhancer in glioblastoma.
# The simulation will model the effects of TNFAIP3 (A20) on glioblastoma stem cells (GSCs) and their tumorigenic potential.

from simulation_utils import GameObject, Container

class GlioblastomaStemCell(GameObject):
    def __init__(self, name, A20_expression=0, survival_rate=0):
        super().__init__(name)
        self.properties = {
            "A20_expression": A20_expression,  # Level of A20 expression
            "survival_rate": survival_rate,    # Survival rate of the GSCs
            "tumorigenic_potential": 0          # Tumorigenic potential
        }

    def tick(self):
        # The tumorigenic potential increases with A20 expression
        self.properties["tumorigenic_potential"] = self.properties["A20_expression"] * self.properties["survival_rate"]

class A20Targeting(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def target(self, gsc):
        # Targeting A20 decreases its expression and survival rate
        gsc.properties["A20_expression"] -= 1
        gsc.properties["survival_rate"] -= 0.1  # Decrease survival rate by 10%
        return f"{gsc.name} A20 expression and survival rate decreased."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("glioblastoma_environment")
        gsc1 = GlioblastomaStemCell("GSC_1", A20_expression=5, survival_rate=0.9)  # High A20 expression
        gsc2 = GlioblastomaStemCell("GSC_2", A20_expression=2, survival_rate=0.5)  # Lower A20 expression
        targeting = A20Targeting("A20_Targeting")
        world.addObject(gsc1)
        world.addObject(gsc2)
        world.addObject(targeting)
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
        self.addAction("target A20 in GSC_1", ["target", allObjects["GSC_1"][0]])
        self.addAction("target A20 in GSC_2", ["target", allObjects["GSC_2"][0]])

    def actionTarget(self, gsc):
        if type(gsc) != GlioblastomaStemCell:
            return f"Cannot target A20 in {gsc.name}."
        else:
            return gsc.properties["A20_expression"], gsc.properties["survival_rate"]

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb.startswith("target"):
            gsc = action[1]
            result = gsc.target(gsc)
            self.observationStr = result
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
    actions = ["look", "target A20 in GSC_1", "target A20 in GSC_2"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the tumorigenic potential after targeting A20
    gsc1 = simulation.rootObject.containsItemWithName("GSC_1")[0]
    gsc2 = simulation.rootObject.containsItemWithName("GSC_2")[0]
    print(f"GSC_1 tumorigenic potential: {gsc1.properties['tumorigenic_potential']}")
    print(f"GSC_2 tumorigenic potential: {gsc2.properties['tumorigenic_potential']}")

    # Determine if the claim is supported or refuted
    if gsc1.properties['tumorigenic_potential'] > 0 and gsc2.properties['tumorigenic_potential'] > 0:
        print("Claim Supported: TNFAIP3 acts as a tumor enhancer in glioblastoma.")
    else:
        print("Claim Refuted: TNFAIP3 does not act as a tumor enhancer in glioblastoma.")

if __name__ == "__main__":
    main()
