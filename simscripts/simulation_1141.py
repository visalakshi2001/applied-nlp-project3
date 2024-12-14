
# Claim: Taking 400mg of α-tocopheryl acetate in combination with vitamin C reduces the risk of prostate cancer.
# The simulation will evaluate the effects of vitamin E and vitamin C on prostate cancer risk based on the provided reference text.

from simulation_utils import GameObject, Container

class Vitamin(GameObject):
    def __init__(self, name, dosage, effect_on_cancer):
        super().__init__(name)
        self.dosage = dosage
        self.effect_on_cancer = effect_on_cancer  # This will be a boolean indicating if it reduces cancer risk

    def tick(self):
        # Simulate the effect of the vitamin on cancer risk
        if self.effect_on_cancer:
            self.properties["cancer_risk"] = "reduced"
        else:
            self.properties["cancer_risk"] = "not reduced"

    def makeDescriptionStr(self):
        return f"{self.name} at {self.dosage} dosage has {self.properties.get('cancer_risk', 'unknown')} effect on cancer risk."

class ProstateCancerRisk(GameObject):
    def __init__(self):
        super().__init__("Prostate Cancer Risk")
        self.risk_level = "normal"  # Initial risk level

    def evaluate_risk(self, vitamins):
        # Evaluate the combined effect of vitamins on prostate cancer risk
        for vitamin in vitamins:
            if vitamin.effect_on_cancer:
                self.risk_level = "reduced"
                return
        self.risk_level = "not reduced"

    def makeDescriptionStr(self):
        return f"Current prostate cancer risk level is: {self.risk_level}."

class World(Container):
    def __init__(self):
        super().__init__("environment")

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
        vitamin_e = Vitamin("Vitamin E", "400 IU every other day", False)  # No effect on cancer risk
        vitamin_c = Vitamin("Vitamin C", "500 mg daily", False)  # No effect on cancer risk
        cancer_risk = ProstateCancerRisk()

        world.addObject(vitamin_e)
        world.addObject(vitamin_c)
        world.addObject(cancer_risk)

        # Evaluate the cancer risk based on the vitamins
        cancer_risk.evaluate_risk([vitamin_e, vitamin_c])
        
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
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
