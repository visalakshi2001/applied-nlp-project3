
# Claim: Drosophila supracellular actomyosin structures are found at boundaries in wing imaginal discs.
# The simulation will check for the presence of Myosin II at the dorsal-ventral boundary in Drosophila wing imaginal discs.

from simulation_utils import GameObject, Container

class Myosin(GameObject):
    def __init__(self, name, location):
        super().__init__(name)
        self.properties = {
            "location": location,
            "isAccumulated": False
        }

    def accumulate(self):
        self.properties["isAccumulated"] = True

    def makeDescriptionStr(self):
        return f"{self.name} located at {self.properties['location']} with accumulation status: {self.properties['isAccumulated']}."

class DrosophilaWing(Container):
    def __init__(self):
        super().__init__("Drosophila Wing")
        self.dorsal_boundary = Myosin("Myosin II", "dorsal-ventral boundary")
        self.addObject(self.dorsal_boundary)

    def simulateNotchSignaling(self):
        # Simulate the activation of Notch signaling which leads to Myosin accumulation
        self.dorsal_boundary.accumulate()

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        wing = DrosophilaWing()
        return wing

    def run_simulation(self):
        # Simulate Notch signaling
        self.rootObject.simulateNotchSignaling()

    def check_claim(self):
        # Check if Myosin II is accumulated at the dorsal-ventral boundary
        if self.rootObject.dorsal_boundary.properties["isAccumulated"]:
            return "Claim Supported: Myosin II is found at the dorsal-ventral boundary."
        else:
            return "Claim Refuted: Myosin II is not found at the dorsal-ventral boundary."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
