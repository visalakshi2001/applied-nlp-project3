
# Claim: The risk of breast cancer among parous women decreases with placental weight of pregnancies.
# The simulation will model the relationship between placental weight and breast cancer risk.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, placental_weight):
        super().__init__(name)
        self.placental_weight = placental_weight  # in grams
        self.breast_cancer_risk = self.calculate_breast_cancer_risk()

    def calculate_breast_cancer_risk(self):
        # Risk increases with placental weight
        if self.placental_weight < 500:
            return "low"
        elif 500 <= self.placental_weight < 700:
            return "moderate"
        else:
            return "high"

    def makeDescriptionStr(self):
        return f"{self.name} has a placental weight of {self.placental_weight}g and a breast cancer risk level of {self.breast_cancer_risk}."

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

    def _initialize_simulation(self):
        world = World()
        woman1 = Woman("Woman A", 450)  # low risk
        woman2 = Woman("Woman B", 600)  # moderate risk
        woman3 = Woman("Woman C", 750)  # high risk
        world.addObject(woman1)
        world.addObject(woman2)
        world.addObject(woman3)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
