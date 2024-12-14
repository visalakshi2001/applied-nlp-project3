
# Claim: Smc5/6 engagement halts the activation of SUMO E3 ligase Mms21 by ATP-dependent remodeling.
# The simulation will test the relationship between Smc5/6 and Mms21 in the context of ATP-dependent remodeling.

from simulation_utils import GameObject, Container

class Smc5(GameObject):
    def __init__(self, name, atp_bound=False):
        super().__init__(name)
        self.properties = {
            "atp_bound": atp_bound
        }

    def bind_atp(self):
        self.properties["atp_bound"] = True

    def unbind_atp(self):
        self.properties["atp_bound"] = False

class Mms21(GameObject):
    def __init__(self, name, activated=False):
        super().__init__(name)
        self.properties = {
            "activated": activated
        }

    def activate(self):
        self.properties["activated"] = True

    def deactivate(self):
        self.properties["activated"] = False

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.test_claim()

    def _initialize_simulation(self):
        world = Container("cell")
        smc5 = Smc5("Smc5")
        mms21 = Mms21("Mms21")
        world.addObject(smc5)
        world.addObject(mms21)
        return world

    def test_claim(self):
        smc5 = self.rootObject.containsItemWithName("Smc5")[0]
        mms21 = self.rootObject.containsItemWithName("Mms21")[0]

        # Simulate ATP binding
        smc5.bind_atp()

        # Check if Mms21 can be activated
        if smc5.properties["atp_bound"]:
            mms21.activate()

        # If Mms21 is activated, the claim is refuted
        if mms21.properties["activated"]:
            return "Refuted: Mms21 is activated despite Smc5/6 engagement."
        else:
            return "Supported: Mms21 remains inactive due to Smc5/6 engagement."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
