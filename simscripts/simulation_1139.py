
# Claim: Taking 400mg of α-tocopheryl acetate does not prevent prostate cancer.
# The simulation will evaluate the effect of vitamin E on prostate cancer incidence based on the provided reference text.

from simulation_utils import GameObject, Container

class Vitamin(GameObject):
    def __init__(self, name, dosage, effect_on_cancer):
        super().__init__(name)
        self.dosage = dosage
        self.effect_on_cancer = effect_on_cancer  # True if it reduces cancer risk, False otherwise

    def tick(self):
        # Simulate the effect of the vitamin on cancer risk
        if self.effect_on_cancer:
            self.properties["cancer_risk"] = "reduced"
        else:
            self.properties["cancer_risk"] = "not reduced"

    def makeDescriptionStr(self):
        return f"{self.name} at {self.dosage} dosage has an effect on cancer risk: {self.properties.get('cancer_risk', 'unknown')}."

class ProstateCancerRisk(GameObject):
    def __init__(self):
        super().__init__("Prostate Cancer Risk")
        self.properties["risk_level"] = "unknown"

    def update_risk(self, vitamin):
        if vitamin.effect_on_cancer:
            self.properties["risk_level"] = "reduced"
        else:
            self.properties["risk_level"] = "not reduced"

    def makeDescriptionStr(self):
        return f"Current prostate cancer risk level is: {self.properties['risk_level']}."

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
        vitamin_e = Vitamin("Vitamin E", "400 IU", False)  # Based on the reference text, it does not reduce cancer risk
        prostate_cancer_risk = ProstateCancerRisk()
        
        world.addObject(vitamin_e)
        world.addObject(prostate_cancer_risk)
        
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
        
        # Update the prostate cancer risk based on the vitamin effect
        vitamin_e = self.rootObject.contains[0]  # Assuming the first object is Vitamin E
        prostate_cancer_risk = self.rootObject.contains[1]  # Assuming the second object is Prostate Cancer Risk
        prostate_cancer_risk.update_risk(vitamin_e)
        vitamin_e.tick()

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
