
# Claim: Integrated care is successful at tackling multiple comorbidities.
# The simulation will evaluate the effectiveness of integrated care in improving quality of life and reducing disability.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, disability_score=0, quality_of_life=0):
        super().__init__(name)
        self.properties = {
            "disability_score": disability_score,
            "quality_of_life": quality_of_life
        }

    def tick(self):
        # Simulate the effect of integrated care
        self.properties["disability_score"] -= 0.9  # Improvement in disability
        self.properties["quality_of_life"] += 0.7   # Improvement in quality of life

    def makeDescriptionStr(self):
        description = f"{self.name} has a disability score of {self.properties['disability_score']} and a quality of life rating of {self.properties['quality_of_life']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "healthcare environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.doWorldTick()

    def _initialize_simulation(self):
        world = World()
        patient1 = Patient("Patient 1", disability_score=5, quality_of_life=2)
        world.addObject(patient1)        
        return world

    def doWorldTick(self):
        # Get a list of all objects in the environment
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        # Loop through all objects, and call their tick()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Check the results after the tick
    patient = simulation.rootObject.contains[0]  # Get the first patient
    if patient.properties["disability_score"] < 5 and patient.properties["quality_of_life"] > 2:
        print("Claim Supported: Integrated care is successful at tackling multiple comorbidities.")
    else:
        print("Claim Refuted: Integrated care is not successful at tackling multiple comorbidities.")

if __name__ == "__main__":
    main()
