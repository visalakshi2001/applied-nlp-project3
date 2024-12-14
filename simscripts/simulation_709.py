
# Claim: Long chain polyunsaturated fatty acids supplementation is associated with lower rates of atopic eczema at 1 year.

from simulation_utils import GameObject, Container

class Infant(GameObject):
    def __init__(self, name, has_atopic_eczema=False):
        super().__init__(name)
        self.properties = {
            "has_atopic_eczema": has_atopic_eczema
        }

    def tick(self):
        # Simulate the effect of LCPUFA supplementation
        if self.properties["has_atopic_eczema"]:
            # If the infant has eczema, there's a chance it could be reduced
            if random.random() < 0.5:  # 50% chance of improvement
                self.properties["has_atopic_eczema"] = False

    def makeDescriptionStr(self):
        return f"{self.name} has atopic eczema: {self.properties['has_atopic_eczema']}."

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
        # Create infants with and without LCPUFA supplementation
        infant_with_supplementation = Infant("Infant with LCPUFA", has_atopic_eczema=True)
        infant_without_supplementation = Infant("Infant without LCPUFA", has_atopic_eczema=True)
        world.addObject(infant_with_supplementation)
        world.addObject(infant_without_supplementation)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"tick": []}

    def step(self, actionStr):
        if actionStr in self.possibleActions:
            # Perform a tick to simulate the passage of time
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()
        else:
            self.observationStr = "ERROR: Unknown action."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the passage of time
    for _ in range(5):  # Simulate 5 time steps
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the final state of the infants
    infants = simulation.rootObject.getAllContainedObjectsRecursive()
    eczema_rates = [infant.properties["has_atopic_eczema"] for infant in infants]
    if eczema_rates.count(True) < len(eczema_rates) / 2:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
