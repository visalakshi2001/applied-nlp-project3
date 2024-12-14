
# Claim: Pro-inflammatory cytokines are up regulated during tumor development.
# The simulation will model the levels of pro-inflammatory cytokines (TNF-alpha and IL-6) in NSCLC patients compared to controls.

from simulation_utils import GameObject, Container

class Cytokine(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.level = level

    def tick(self):
        # Simulate the increase in cytokine levels in NSCLC patients
        if self.name == "TNF-alpha":
            self.level += 44.1  # Simulating the level in NSCLC patients
        elif self.name == "IL-6":
            self.level += 6.4  # Simulating a baseline level

    def makeDescriptionStr(self):
        return f"{self.name} level is {self.level:.2f} pg/mL."

class Patient(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.cytokines = {
            "TNF-alpha": Cytokine("TNF-alpha"),
            "IL-6": Cytokine("IL-6")
        }

    def tick(self):
        for cytokine in self.cytokines.values():
            cytokine.tick()

    def makeDescriptionStr(self):
        description = f"{self.name} has the following cytokine levels:\n"
        for cytokine in self.cytokines.values():
            description += "\t" + cytokine.makeDescriptionStr() + "\n"
        return description

class ControlGroup(Patient):
    def __init__(self):
        super().__init__("Control Group")
        self.cytokines["TNF-alpha"].level = 15.1  # Control level
        self.cytokines["IL-6"].level = 4.1  # Control level

class NSCLCGroup(Patient):
    def __init__(self):
        super().__init__("NSCLC Group")

class World(Container):
    def __init__(self):
        super().__init__("Cytokine Environment")
        self.nsclc_patient = NSCLCGroup()
        self.control_patient = ControlGroup()
        self.addObject(self.nsclc_patient)
        self.addObject(self.control_patient)

    def makeDescriptionStr(self):
        return self.nsclc_patient.makeDescriptionStr() + self.control_patient.makeDescriptionStr()

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def run_simulation(self):
        # Simulate the environment for a certain number of ticks
        for _ in range(1):  # Run for 1 tick
            self.rootObject.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
