
# Claim: Rhythmic expression of Cry1 translates directly into a circadian regulation of cAMP signaling in hepatic glucose metabolism.

from simulation_utils import GameObject, Container

class CryProtein(GameObject):
    def __init__(self, name, expression_level=0, cAMP_level=0):
        super().__init__(name)
        self.properties = {
            "expression_level": expression_level,  # Rhythmic expression level
            "cAMP_level": cAMP_level,              # cAMP signaling level
        }

    def tick(self):
        # Simulate the rhythmic expression of Cry1
        self.properties["expression_level"] = (self.properties["expression_level"] + 1) % 24  # Simulating a 24-hour cycle
        # cAMP level is inversely related to Cry1 expression
        self.properties["cAMP_level"] = 10 - (self.properties["expression_level"] / 2)  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"{self.name} has an expression level of {self.properties['expression_level']} and cAMP level of {self.properties['cAMP_level']}."

class Gluconeogenesis(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.properties = {
            "activity_level": activity_level,  # Level of gluconeogenesis activity
        }

    def tick(self, cAMP_level):
        # Gluconeogenesis activity is directly influenced by cAMP levels
        self.properties["activity_level"] = cAMP_level * 2  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"Gluconeogenesis activity level is {self.properties['activity_level']}."

class Liver(Container):
    def __init__(self):
        super().__init__("Liver")
        self.cry1 = CryProtein("Cry1")
        self.gluconeogenesis = Gluconeogenesis("Gluconeogenesis")
        self.addObject(self.cry1)
        self.addObject(self.gluconeogenesis)

    def tick(self):
        self.cry1.tick()
        self.gluconeogenesis.tick(self.cry1.properties["cAMP_level"])

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.liver = Liver()
        self.addObject(self.liver)

    def makeDescriptionStr(self):
        return f"In the {self.name}, you see: \n" + self.liver.makeDescriptionStr() + "\n" + self.liver.cry1.makeDescriptionStr()

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def step(self):
        self.rootObject.tick()
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    for _ in range(24):  # Simulate for 24 hours
        print("Next hour:")
        obs = simulation.step()
        print(obs)
        print()

if __name__ == "__main__":
    main()
