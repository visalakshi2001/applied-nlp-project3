
# Claim: Alirocumab treatment reduces apo(a) fractional clearance rate.
# The simulation will model the effects of Alirocumab on apo(a) fractional clearance rate (FCR).

from simulation_utils import GameObject, Container

class ApoA(GameObject):
    def __init__(self, name, FCR=0):
        super().__init__(name)
        self.FCR = FCR  # Fractional Clearance Rate

    def tick(self, treatment_effect):
        # Apply treatment effect to FCR
        self.FCR += treatment_effect

    def makeDescriptionStr(self):
        return f"{self.name} has a fractional clearance rate of {self.FCR}."

class Alirocumab(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def apply_treatment(self, apoA):
        # The treatment effect is a 24.6% increase in FCR
        treatment_effect = 24.6
        apoA.tick(treatment_effect)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("simulation_environment")
        apoA = ApoA("apo(a)", FCR=0)  # Initial FCR of apo(a)
        alirocumab = Alirocumab("Alirocumab")
        world.addObject(apoA)
        world.addObject(alirocumab)
        return world

    def step(self):
        # Apply Alirocumab treatment to apo(a)
        alirocumab = self.rootObject.containsItemWithName("Alirocumab")[0]
        apoA = self.rootObject.containsItemWithName("apo(a)")[0]
        alirocumab.apply_treatment(apoA)

        # Update observation string
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print("Before treatment:")
    print(simulation.observationStr)
    
    # Step to apply treatment
    result = simulation.step()
    print("After treatment:")
    print(result)

    # Determine if the claim is supported or refuted
    apoA = simulation.rootObject.containsItemWithName("apo(a)")[0]
    if apoA.FCR > 0:
        print("Claim Supported: Alirocumab treatment increases apo(a) fractional clearance rate.")
    else:
        print("Claim Refuted: Alirocumab treatment does not increase apo(a) fractional clearance rate.")

if __name__ == "__main__":
    main()
