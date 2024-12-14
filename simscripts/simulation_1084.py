
# Claim: Side effects associated with antidepressants increases risk of stroke.
# The simulation will model the relationship between antidepressant use and the risk of stroke in older adults.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, age, antidepressant_type=None):
        super().__init__(name)
        self.age = age
        self.antidepressant_type = antidepressant_type
        self.stroke_risk = 1.0  # baseline risk

    def take_antidepressant(self, antidepressant_type):
        self.antidepressant_type = antidepressant_type
        if antidepressant_type == "other":
            self.stroke_risk *= 1.37  # increase risk by 37%
        elif antidepressant_type == "SSRI":
            self.stroke_risk *= 1.0  # no increase in risk
        elif antidepressant_type == "tricyclic":
            self.stroke_risk *= 1.0  # no increase in risk

    def makeDescriptionStr(self):
        return f"{self.name}, age {self.age}, taking {self.antidepressant_type} with stroke risk of {self.stroke_risk:.2f}."

class World(Container):
    def __init__(self):
        super().__init__("environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        patient1 = Patient("Patient 1", 70)
        patient2 = Patient("Patient 2", 75)
        
        # Patient 1 takes an "other" antidepressant
        patient1.take_antidepressant("other")
        
        # Patient 2 takes an SSRI
        patient2.take_antidepressant("SSRI")
        
        world.addObject(patient1)
        world.addObject(patient2)
        
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
