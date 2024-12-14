
# Claim: Cardiac tissue-resident macrophages directly contribute to electrical activity.
# The simulation will model cardiac macrophages and their interaction with cardiomyocytes to determine if they contribute to electrical activity.

from simulation_utils import GameObject, Container

class Macrophage(GameObject):
    def __init__(self, name, connexin_43=True):
        super().__init__(name)
        self.properties = {
            "connexin_43": connexin_43,
            "resting_membrane_potential": -70,  # in mV, typical for macrophages
            "depolarization": False
        }

    def tick(self, cardiomyocyte):
        if self.properties["connexin_43"]:
            # Facilitate electrical conduction
            self.properties["depolarization"] = True
            cardiomyocyte.properties["resting_membrane_potential"] += 10  # Make cardiomyocyte more positive
            cardiomyocyte.properties["repolarization_speed"] += 1  # Accelerate repolarization

class Cardiomyocyte(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "resting_membrane_potential": -80,  # in mV, typical for cardiomyocytes
            "repolarization_speed": 1  # baseline speed
        }

    def tick(self):
        if self.properties["repolarization_speed"] > 1:
            self.properties["resting_membrane_potential"] -= 5  # Repolarization effect

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("heart")
        macrophage = Macrophage("cardiac_macrophage")
        cardiomyocyte = Cardiomyocyte("cardiomyocyte")
        world.addObject(macrophage)
        world.addObject(cardiomyocyte)
        return world

    def run_simulation(self):
        macrophage = self.rootObject.containsItemWithName("cardiac_macrophage")[0]
        cardiomyocyte = self.rootObject.containsItemWithName("cardiomyocyte")[0]

        # Simulate interaction
        macrophage.tick(cardiomyocyte)
        cardiomyocyte.tick()

        # Check results
        if macrophage.properties["depolarization"] and cardiomyocyte.properties["resting_membrane_potential"] > -80:
            self.observationStr = "Claim Supported: Cardiac macrophages contribute to electrical activity."
        else:
            self.observationStr = "Claim Refuted: Cardiac macrophages do not contribute to electrical activity."

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
