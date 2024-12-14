
# Claim: PCSK9 inhibitors decrease plasma Lp(a) levels.
# Simulation to verify the claim based on the provided reference text.

from simulation_utils import GameObject, Container

class PCSK9Inhibitor(GameObject):
    def __init__(self, name, effect_on_Lp_a=0):
        super().__init__(name)
        self.effect_on_Lp_a = effect_on_Lp_a  # Effect on plasma Lp(a) levels

    def apply_effect(self):
        # Simulate the effect of the PCSK9 inhibitor on Lp(a) levels
        self.effect_on_Lp_a = -18.7  # Represents a decrease of 18.7% in plasma Lp(a)

class Participant(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.Lp_a_level = 100  # Initial plasma Lp(a) level (arbitrary unit)

    def receive_inhibitor(self, inhibitor):
        inhibitor.apply_effect()
        self.Lp_a_level += inhibitor.effect_on_Lp_a  # Apply the effect of the inhibitor

class World(Container):
    def __init__(self):
        super().__init__("clinical trial environment")

    def makeDescriptionStr(self):
        return f"In the {self.name}, participants are receiving treatment with PCSK9 inhibitors."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.participant = Participant("Participant 1")
        self.inhibitor = PCSK9Inhibitor("Alirocumab")

    def _initialize_simulation(self):
        world = World()
        world.addObject(self.participant)
        return world

    def run_trial(self):
        self.participant.receive_inhibitor(self.inhibitor)
        return self.participant.Lp_a_level

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    final_Lp_a_level = simulation.run_trial()
    print(f"Final plasma Lp(a) level after treatment: {final_Lp_a_level}")

    # Determine if the claim is supported or refuted
    if final_Lp_a_level < 100:  # Since we started with 100, a decrease indicates support for the claim
        print("Claim Supported: PCSK9 inhibitors decrease plasma Lp(a) levels.")
    else:
        print("Claim Refuted: PCSK9 inhibitors do not decrease plasma Lp(a) levels.")

if __name__ == "__main__":
    main()
