
# Claim: A high microerythrocyte count protects against severe anemia in homozygous alpha (+)- thalassemia trait subjects.
# The simulation will model the relationship between erythrocyte count and the risk of severe malaria anemia (SMA) in subjects with homozygous alpha(+)-thalassemia.

from simulation_utils import GameObject, Container

class Erythrocyte(GameObject):
    def __init__(self, count):
        super().__init__("erythrocyte")
        self.count = count  # Number of erythrocytes
        self.hb_concentration = 100  # Initial hemoglobin concentration in g/l

    def tick(self):
        # Simulate the effect of malaria on erythrocyte count
        self.count -= 1.5  # Simulating a loss of erythrocytes due to malaria
        if self.count < 0:
            self.count = 0  # Prevent negative erythrocyte count

    def makeDescriptionStr(self):
        return f"Erythrocyte count: {self.count}, Hemoglobin concentration: {self.hb_concentration} g/l"

class ThalassemiaSubject(GameObject):
    def __init__(self, name, erythrocyte_count):
        super().__init__(name)
        self.erythrocyte = Erythrocyte(erythrocyte_count)

    def tick(self):
        self.erythrocyte.tick()

    def makeDescriptionStr(self):
        return f"{self.name} - " + self.erythrocyte.makeDescriptionStr()

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

    def _initialize_simulation(self):
        world = World()
        subject1 = ThalassemiaSubject("Subject 1", 5.0)  # High erythrocyte count
        subject2 = ThalassemiaSubject("Subject 2", 3.0)  # Lower erythrocyte count
        world.addObject(subject1)
        world.addObject(subject2)
        return world

    def step(self):
        self.rootObject.tick()
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate a few time steps to observe the effects
    for _ in range(3):
        print("After malaria impact:")
        print(simulation.step())
        print()

if __name__ == "__main__":
    main()
