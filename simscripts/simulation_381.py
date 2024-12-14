
# Claim: Environmental factors can influence the development of breast cancer.
# This simulation will test the interaction between genetic susceptibility polymorphisms and environmental factors in relation to breast cancer incidence.

from simulation_utils import GameObject, Container

class EnvironmentalFactor(GameObject):
    def __init__(self, name, influence_level=0):
        super().__init__(name)
        self.properties = {
            "influence_level": influence_level  # Represents the level of influence on breast cancer development
        }

    def tick(self):
        # Simulate the effect of the environmental factor over time
        self.properties["influence_level"] += 1  # Increment influence level as a simple simulation

    def makeDescriptionStr(self):
        return f"{self.name} with influence level {self.properties['influence_level']}."

class GeneticPolymorphism(GameObject):
    def __init__(self, name, risk_factor=0):
        super().__init__(name)
        self.properties = {
            "risk_factor": risk_factor  # Represents the risk factor associated with this genetic polymorphism
        }

    def tick(self):
        # Simulate the effect of the genetic polymorphism over time
        self.properties["risk_factor"] += 0.5  # Increment risk factor as a simple simulation

    def makeDescriptionStr(self):
        return f"{self.name} with risk factor {self.properties['risk_factor']}."

class BreastCancerRisk(GameObject):
    def __init__(self):
        super().__init__("Breast Cancer Risk")
        self.environmental_factors = []
        self.genetic_polymorphisms = []

    def addEnvironmentalFactor(self, factor):
        self.environmental_factors.append(factor)

    def addGeneticPolymorphism(self, polymorphism):
        self.genetic_polymorphisms.append(polymorphism)

    def calculateRisk(self):
        total_risk = 0
        for factor in self.environmental_factors:
            total_risk += factor.properties["influence_level"]
        for polymorphism in self.genetic_polymorphisms:
            total_risk += polymorphism.properties["risk_factor"]
        return total_risk

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.breast_cancer_risk = BreastCancerRisk()

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += f"Total Breast Cancer Risk: {self.breast_cancer_risk.calculateRisk()}\n"
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
        # Adding environmental factors
        age_at_menarche = EnvironmentalFactor("Age at Menarche", influence_level=2)
        body_mass_index = EnvironmentalFactor("Body Mass Index", influence_level=3)
        alcohol_consumption = EnvironmentalFactor("Alcohol Consumption", influence_level=4)

        # Adding genetic polymorphisms
        fgfr2 = GeneticPolymorphism("FGFR2 Polymorphism", risk_factor=1)
        tnrc9 = GeneticPolymorphism("TNRC9 Polymorphism", risk_factor=1.5)

        # Adding objects to the world
        world.addObject(age_at_menarche)
        world.addObject(body_mass_index)
        world.addObject(alcohol_consumption)
        world.breast_cancer_risk.addEnvironmentalFactor(age_at_menarche)
        world.breast_cancer_risk.addEnvironmentalFactor(body_mass_index)
        world.breast_cancer_risk.addEnvironmentalFactor(alcohol_consumption)
        world.breast_cancer_risk.addGeneticPolymorphism(fgfr2)
        world.breast_cancer_risk.addGeneticPolymorphism(tnrc9)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Update the environment
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

if __name__ == "__main__":
    main()

# The output of the simulation will show the total breast cancer risk based on the environmental factors and genetic polymorphisms.
# If the total risk is influenced by the environmental factors, it supports the claim.
