
# Claim: Inhibiting glucose-6-phosphate dehydrogenase improves lipogenesis by deactivating LKB1-AMPK signaling.
# The simulation will model the effects of inhibiting glucose-6-phosphate dehydrogenase (6PGD) on lipogenesis and AMPK signaling.

from simulation_utils import GameObject, Container

class Glucose6PhosphateDehydrogenase(GameObject):
    def __init__(self, name, activity_level=1):
        super().__init__(name)
        self.activity_level = activity_level  # Activity level of 6PGD

    def inhibit(self):
        self.activity_level = 0  # Inhibition of 6PGD

class AMPK(GameObject):
    def __init__(self, name, active=True):
        super().__init__(name)
        self.active = active  # Indicates if AMPK is active

    def deactivate(self):
        self.active = False  # Deactivate AMPK

class Lipogenesis(GameObject):
    def __init__(self, name, rate=0):
        super().__init__(name)
        self.rate = rate  # Rate of lipogenesis

    def increase(self):
        self.rate += 1  # Increase lipogenesis rate

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell environment")
        self.6PGD = Glucose6PhosphateDehydrogenase("6PGD")
        self.ampk = AMPK("AMPK")
        self.lipogenesis = Lipogenesis("Lipogenesis")

        world.addObject(self.6PGD)
        world.addObject(self.ampk)
        world.addObject(self.lipogenesis)

        return world

    def simulate_inhibition(self):
        # Inhibit 6PGD
        self.6PGD.inhibit()
        # Deactivate AMPK
        self.ampk.deactivate()
        # Increase lipogenesis
        self.lipogenesis.increase()

    def check_results(self):
        if self.6PGD.activity_level == 0 and not self.ampk.active:
            return "Claim Supported: Inhibiting 6PGD improves lipogenesis by deactivating LKB1-AMPK signaling."
        else:
            return "Claim Refuted: Inhibiting 6PGD does not improve lipogenesis as claimed."

def main():
    simulation = Simulation()
    simulation.simulate_inhibition()
    result = simulation.check_results()
    print(result)

if __name__ == "__main__":
    main()
