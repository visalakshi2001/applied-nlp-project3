
# Claim: Rhythmic expression of Cry1 translates directly into a circadian regulation of cAMP signaling in gluconeogenesis.
# The simulation will model the relationship between Cry1 expression, cAMP levels, and gluconeogenesis.

from simulation_utils import GameObject, Container

class CryProtein(GameObject):
    def __init__(self, name, expression_level=0):
        super().__init__(name)
        self.properties = {
            "expression_level": expression_level  # Rhythmic expression level of Cry1
        }

    def tick(self):
        # Simulate the rhythmic expression of Cry1
        # For simplicity, we will alternate expression levels to simulate day/night cycles
        if self.properties["expression_level"] == 0:
            self.properties["expression_level"] = 1  # Elevated expression during night
        else:
            self.properties["expression_level"] = 0  # Low expression during day

class cAMP(GameObject):
    def __init__(self, name, concentration=0):
        super().__init__(name)
        self.properties = {
            "concentration": concentration  # cAMP concentration
        }

    def tick(self, cry_protein):
        # cAMP concentration is affected by Cry1 expression
        if cry_protein.properties["expression_level"] == 1:
            self.properties["concentration"] = max(0, self.properties["concentration"] - 1)  # Cry1 reduces cAMP
        else:
            self.properties["concentration"] += 1  # cAMP increases when Cry1 is low

class Gluconeogenesis(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.properties = {
            "activity_level": activity_level  # Activity level of gluconeogenesis
        }

    def tick(self, cAMP):
        # Gluconeogenesis activity is inversely related to cAMP concentration
        self.properties["activity_level"] = max(0, 10 - cAMP.properties["concentration"])  # Max activity when cAMP is low

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
        cry1 = CryProtein("Cry1")
        camp = cAMP("cAMP")
        gluconeogenesis = Gluconeogenesis("Gluconeogenesis")
        world.addObject(cry1)
        world.addObject(camp)
        world.addObject(gluconeogenesis)
        return world

    def step(self):
        # Perform one tick for each object
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, CryProtein):
                obj.tick()
            elif isinstance(obj, cAMP):
                obj.tick(cry1)
            elif isinstance(obj, Gluconeogenesis):
                obj.tick(camp)

        # Update the observation string
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate for a few cycles to observe the changes
    for _ in range(5):
        print("Tick:")
        obs = simulation.step()
        print(obs)

if __name__ == "__main__":
    main()
