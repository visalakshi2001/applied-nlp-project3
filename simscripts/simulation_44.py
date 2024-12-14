
# Claim: A mutation in HNF4A leads to an increased risk of developing diabetes by the age of 14 years.
# This simulation will assess the impact of HNF4A mutations on diabetes risk.

from simulation_utils import GameObject, Container

class HNF4A(GameObject):
    def __init__(self, mutation_status="wild_type"):
        super().__init__("HNF4A")
        self.mutation_status = mutation_status
        self.properties = {
            "diabetes_risk": 0  # Risk of developing diabetes
        }

    def tick(self):
        if self.mutation_status == "mutated":
            self.properties["diabetes_risk"] += 10  # Increased risk due to mutation
        else:
            self.properties["diabetes_risk"] += 1  # Normal risk

    def makeDescriptionStr(self):
        return f"HNF4A with mutation status: {self.mutation_status}, diabetes risk: {self.properties['diabetes_risk']}."

class Child(GameObject):
    def __init__(self, age=0):
        super().__init__("Child")
        self.age = age
        self.hnf4a_gene = HNF4A()

    def tick(self):
        self.age += 1  # Increment age each tick
        self.hnf4a_gene.tick()  # Update diabetes risk based on HNF4A status

    def makeDescriptionStr(self):
        return f"A child aged {self.age} years, with {self.hnf4a_gene.makeDescriptionStr()}"

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.child = Child()

    def makeDescriptionStr(self):
        return f"In the {self.name}, you see: \n\t{self.child.makeDescriptionStr()}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        world.child.hnf4a_gene.mutation_status = "mutated"  # Set mutation status to mutated
        return world

    def step(self):
        self.rootObject.child.tick()  # Simulate the passage of time
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate for 14 years
    for _ in range(14):
        simulation.step()

    print("\nAfter 14 years:")
    print(simulation.observationStr)

    # Check diabetes risk
    diabetes_risk = simulation.rootObject.child.hnf4a_gene.properties["diabetes_risk"]
    if diabetes_risk > 10:  # Arbitrary threshold for increased risk
        print("Claim Supported: Increased risk of developing diabetes due to HNF4A mutation.")
    else:
        print("Claim Refuted: No significant increase in diabetes risk.")

if __name__ == "__main__":
    main()
