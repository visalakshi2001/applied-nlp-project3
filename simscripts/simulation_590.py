
# Claim: In young and middle-aged adults, current or remote uses of ADHD medications increase the risk of serious cardiovascular events.
# The simulation will evaluate the risk of serious cardiovascular events based on the use of ADHD medications.

from simulation_utils import GameObject, Container

class Adult(GameObject):
    def __init__(self, age, medication_use="none"):
        super().__init__("adult")
        self.age = age
        self.medication_use = medication_use
        self.cardiovascular_events = 0

    def evaluate_risk(self):
        if self.medication_use == "current":
            # Current use of ADHD medications
            self.cardiovascular_events = 0.83  # Adjusted RR for current use
        elif self.medication_use == "remote":
            # Remote use of ADHD medications
            self.cardiovascular_events = 1.02  # Adjusted RR for new use vs remote use
        else:
            # No use of ADHD medications
            self.cardiovascular_events = 1.0  # Baseline risk

    def makeDescriptionStr(self):
        return f"An adult aged {self.age} with {self.medication_use} ADHD medication use has a cardiovascular event risk of {self.cardiovascular_events}."

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
        adult1 = Adult(age=30, medication_use="current")
        adult2 = Adult(age=45, medication_use="remote")
        adult3 = Adult(age=25, medication_use="none")
        
        adult1.evaluate_risk()
        adult2.evaluate_risk()
        adult3.evaluate_risk()
        
        world.addObject(adult1)
        world.addObject(adult2)
        world.addObject(adult3)
        
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
