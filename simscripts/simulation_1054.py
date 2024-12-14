
# Claim: Risk of cardiovascular events can be cut by a third by using antihypertensive drug therapy among hemodialysis patients.
# The simulation will assess the effect of antihypertensive drug therapy on cardiovascular events among hemodialysis patients.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, on_dialysis=False, receiving_therapy=False):
        super().__init__(name)
        self.properties = {
            "on_dialysis": on_dialysis,
            "receiving_therapy": receiving_therapy,
            "cardiovascular_events": 0
        }

    def apply_therapy(self):
        if self.properties["receiving_therapy"]:
            return f"{self.name} is already receiving therapy."
        self.properties["receiving_therapy"] = True
        return f"{self.name} has started receiving antihypertensive therapy."

    def simulate_events(self):
        if self.properties["receiving_therapy"]:
            # Assuming therapy reduces cardiovascular events by 31% (1/3)
            self.properties["cardiovascular_events"] = int(1 * 0.69)  # 1 event reduced to 0.69
        else:
            self.properties["cardiovascular_events"] = 1  # baseline event

    def makeDescriptionStr(self):
        return f"{self.name}: On dialysis: {self.properties['on_dialysis']}, Receiving therapy: {self.properties['receiving_therapy']}, Cardiovascular events: {self.properties['cardiovascular_events']}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("Dialysis Center")
        patient1 = Patient("Patient A", on_dialysis=True)
        patient2 = Patient("Patient B", on_dialysis=True)
        world.addObject(patient1)
        world.addObject(patient2)
        return world

    def run_simulation(self):
        # Patient A receives therapy
        self.rootObject.contains[0].apply_therapy()  # Patient A
        # Simulate cardiovascular events
        for patient in self.rootObject.contains:
            patient.simulate_events()

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
