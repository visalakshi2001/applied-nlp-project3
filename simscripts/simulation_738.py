
# Claim: MICAL redox enzymes regulate actin dynamics.
# The simulation will demonstrate the relationship between MICAL, CRMP2 oxidation, and actin dynamics.

from simulation_utils import GameObject, Container

class MICAL(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "hydrogen_peroxide": 0,
            "CRMP2_oxidized": False
        }

    def generate_hydrogen_peroxide(self):
        self.properties["hydrogen_peroxide"] += 1

    def oxidize_CRMP2(self):
        if self.properties["hydrogen_peroxide"] > 0:
            self.properties["CRMP2_oxidized"] = True
            self.properties["hydrogen_peroxide"] -= 1

class CRMP2(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_oxidized": False,
            "is_phosphorylated": False
        }

    def oxidize(self):
        self.properties["is_oxidized"] = True

    def phosphorylate(self):
        if self.properties["is_oxidized"]:
            self.properties["is_phosphorylated"] = True

class ActinDynamics(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "dynamics_regulated": False
        }

    def regulate_dynamics(self):
        self.properties["dynamics_regulated"] = True

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("cell_environment")
        mical = MICAL("MICAL")
        crmp2 = CRMP2("CRMP2")
        actin_dynamics = ActinDynamics("Actin Dynamics")

        world.addObject(mical)
        world.addObject(crmp2)
        world.addObject(actin_dynamics)

        return world

    def run_simulation(self):
        # Simulate the process
        mical = self.rootObject.containsItemWithName("MICAL")[0]
        crmp2 = self.rootObject.containsItemWithName("CRMP2")[0]
        actin_dynamics = self.rootObject.containsItemWithName("Actin Dynamics")[0]

        # MICAL generates hydrogen peroxide
        mical.generate_hydrogen_peroxide()
        # MICAL oxidizes CRMP2
        mical.oxidize_CRMP2()
        # CRMP2 oxidizes
        if mical.properties["CRMP2_oxidized"]:
            crmp2.oxidize()
            # CRMP2 phosphorylates
            crmp2.phosphorylate()
            # If phosphorylated, regulate actin dynamics
            if crmp2.properties["is_phosphorylated"]:
                actin_dynamics.regulate_dynamics()

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += f"\t{obj.name}: {obj.properties}\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())
    # Check if the claim is supported
    actin_dynamics = simulation.rootObject.containsItemWithName("Actin Dynamics")[0]
    if actin_dynamics.properties["dynamics_regulated"]:
        print("Claim Supported: MICAL redox enzymes regulate actin dynamics.")
    else:
        print("Claim Refuted: MICAL redox enzymes do not regulate actin dynamics.")

if __name__ == "__main__":
    main()
