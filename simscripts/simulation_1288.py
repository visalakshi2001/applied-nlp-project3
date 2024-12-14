
# Claim: There is a positive correlation between hip fractures and statin use.
# The simulation will test the relationship between statin use and hip fracture risk.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, statin_use=False, hip_fracture=False):
        super().__init__(name)
        self.properties = {
            "statin_use": statin_use,  # Indicates if the patient is using statins
            "hip_fracture": hip_fracture  # Indicates if the patient has a hip fracture
        }

    def tick(self):
        # Simulate the effect of statin use on hip fracture risk
        if self.properties["statin_use"]:
            self.properties["hip_fracture"] = False  # Statin use reduces hip fracture risk

    def makeDescriptionStr(self):
        return f"{self.name}: Statin use = {self.properties['statin_use']}, Hip fracture = {self.properties['hip_fracture']}"

class World(Container):
    def __init__(self):
        super().__init__("hospital")
        # Create patients with different statin use scenarios
        self.addObject(Patient("Patient A", statin_use=True, hip_fracture=False))  # Statin user, no fracture
        self.addObject(Patient("Patient B", statin_use=True, hip_fracture=False))  # Statin user, no fracture
        self.addObject(Patient("Patient C", statin_use=False, hip_fracture=True))  # Non-user, has fracture
        self.addObject(Patient("Patient D", statin_use=False, hip_fracture=True))  # Non-user, has fracture

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def run_simulation(self):
        # Simulate the environment for a number of ticks
        for _ in range(3):  # Run for 3 ticks
            self.rootObject.tick()
            self.observationStr += self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
