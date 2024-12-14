
# Claim: Dscam1 acts as a hypervariable pattern-recognition receptor for the immune system.
# The simulation will model the role of Dscam1 in the immune system of Anopheles gambiae.

from simulation_utils import GameObject, Container

class Dscam(GameObject):
    def __init__(self, name, is_hypervariable=True):
        super().__init__(name)
        self.properties = {
            "is_hypervariable": is_hypervariable,
            "PRR_count": 0
        }

    def generate_PRRs(self, count):
        self.properties["PRR_count"] = count

    def makeDescriptionStr(self):
        description = f"{self.name} is a {'hypervariable' if self.properties['is_hypervariable'] else 'non-hypervariable'} pattern-recognition receptor with {self.properties['PRR_count']} PRRs generated."
        return description

class Pathogen(GameObject):
    def __init__(self, name):
        super().__init__(name)

class ImmuneSystem(Container):
    def __init__(self):
        super().__init__("Immune System")
        self.dscam = Dscam("Dscam1")
        self.addObject(self.dscam)

    def respond_to_infection(self, pathogen):
        self.dscam.generate_PRRs(5)  # Simulating the generation of 5 PRRs in response to infection
        return f"{self.dscam.name} responds to {pathogen.name} by generating PRRs."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        immune_system = ImmuneSystem()
        pathogen = Pathogen("Malaria Parasite")
        immune_system.respond_to_infection(pathogen)
        return immune_system

    def run(self):
        return self.observationStr

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
