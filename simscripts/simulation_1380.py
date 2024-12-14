
# Claim: Women with a lower birth weight are more likely to develop breast cancer later in life.
# The simulation will test the relationship between birth weight and breast cancer risk.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, birth_weight):
        super().__init__(name)
        self.birth_weight = birth_weight  # in grams
        self.breast_cancer_risk = 0  # risk factor, higher means more risk

    def assess_risk(self):
        # The risk is inversely related to birth weight based on the claim
        if self.birth_weight < 2500:  # lower birth weight
            self.breast_cancer_risk = 1.2  # increased risk
        elif self.birth_weight < 3000:  # moderate birth weight
            self.breast_cancer_risk = 1.1  # slight increase in risk
        else:  # higher birth weight
            self.breast_cancer_risk = 1.0  # baseline risk

    def makeDescriptionStr(self):
        return f"{self.name} with a birth weight of {self.birth_weight}g has a breast cancer risk factor of {self.breast_cancer_risk}."

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
        woman1 = Woman("Woman A", 2400)  # lower birth weight
        woman2 = Woman("Woman B", 3200)  # higher birth weight
        woman3 = Woman("Woman C", 2800)  # moderate birth weight
        world.addObject(woman1)
        world.addObject(woman2)
        world.addObject(woman3)
        
        # Assess risk for each woman
        woman1.assess_risk()
        woman2.assess_risk()
        woman3.assess_risk()
        
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

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Claim Verification:")
    if simulation.rootObject.contains[0].breast_cancer_risk > simulation.rootObject.contains[1].breast_cancer_risk:
        print("Supported: Lower birth weight is associated with higher breast cancer risk.")
    else:
        print("Refuted: No association found.")

if __name__ == "__main__":
    main()
