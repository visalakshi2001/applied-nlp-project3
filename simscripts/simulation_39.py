
# Claim: A diminished ovarian reserve does not solely indicate infertility in an a priori non-infertile population.
# The simulation will model women with different ovarian reserve biomarkers and their probabilities of conception.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, AMH, FSH, attempts=6):
        super().__init__(name)
        self.AMH = AMH  # Antimüllerian hormone level
        self.FSH = FSH  # Follicle-stimulating hormone level
        self.attempts = attempts
        self.conception_probability = self.calculate_conception_probability()

    def calculate_conception_probability(self):
        # Simulate the probability of conception based on AMH and FSH levels
        if self.AMH < 0.7:
            return 65  # Probability for low AMH
        elif self.FSH > 10:
            return 63  # Probability for high FSH
        else:
            return 62  # Normal values

    def makeDescriptionStr(self):
        return f"{self.name} with AMH: {self.AMH}, FSH: {self.FSH}, Conception Probability: {self.conception_probability}%."

class World(Container):
    def __init__(self):
        Container.__init__(self, "fertility simulation environment")

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
        # Create women with different ovarian reserve biomarkers
        woman1 = Woman("Woman 1", AMH=0.5, FSH=9)  # Low AMH
        woman2 = Woman("Woman 2", AMH=1.0, FSH=11)  # High FSH
        woman3 = Woman("Woman 3", AMH=0.8, FSH=8)   # Normal values
        world.addObject(woman1)
        world.addObject(woman2)
        world.addObject(woman3)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
