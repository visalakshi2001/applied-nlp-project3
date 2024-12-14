
# Claim: Fibroblast growth factor 21 protects against atherosclerosis by modulating adiponectin and SREBP2 levels.
# The simulation will model the effects of FGF21 on atherosclerosis, adiponectin, and SREBP2 levels.

from simulation_utils import GameObject, Container

class FGF21(GameObject):
    def __init__(self, name, adiponectin_level=0, SREBP2_level=0):
        super().__init__(name)
        self.properties = {
            "adiponectin_level": adiponectin_level,
            "SREBP2_level": SREBP2_level,
            "atherosclerosis_protection": False
        }

    def tick(self):
        # Simulate the effect of FGF21 on adiponectin and SREBP2 levels
        self.properties["adiponectin_level"] += 1  # FGF21 induces adiponectin production
        self.properties["SREBP2_level"] -= 1  # FGF21 suppresses SREBP2 expression

        # Determine if FGF21 is providing protection against atherosclerosis
        if self.properties["adiponectin_level"] > 0 and self.properties["SREBP2_level"] < 5:
            self.properties["atherosclerosis_protection"] = True
        else:
            self.properties["atherosclerosis_protection"] = False

    def makeDescriptionStr(self):
        description = (f"{self.name} has an adiponectin level of {self.properties['adiponectin_level']} "
                       f"and an SREBP2 level of {self.properties['SREBP2_level']}. "
                       f"Atherosclerosis protection status: {self.properties['atherosclerosis_protection']}.")
        return description

class AtherosclerosisSimulation(Container):
    def __init__(self):
        super().__init__("Atherosclerosis Simulation Environment")
        self.fgf21 = FGF21("Fibroblast Growth Factor 21")
        self.addObject(self.fgf21)

    def makeDescriptionStr(self):
        return self.fgf21.makeDescriptionStr()

class Simulation:
    def __init__(self):
        self.rootObject = AtherosclerosisSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def step(self):
        self.rootObject.fgf21.tick()
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    for _ in range(10):  # Simulate for 10 time steps
        result = simulation.step()
        print(result)

    # Final check on the protection status
    if simulation.rootObject.fgf21.properties["atherosclerosis_protection"]:
        print("Claim Supported: FGF21 protects against atherosclerosis.")
    else:
        print("Claim Refuted: FGF21 does not protect against atherosclerosis.")

if __name__ == "__main__":
    main()
