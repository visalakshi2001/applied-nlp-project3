
# Claim: Bacterial meningitis can be diagnosed on the basis of positive cerebrospinal fluid (CSF) cultures.
# The simulation will check if the conditions for diagnosing bacterial meningitis based on CSF analysis are met.

from simulation_utils import GameObject, Container

class CSFAnalysis(GameObject):
    def __init__(self, glucose_ratio, white_cell_count, lactate_level):
        super().__init__("CSF Analysis")
        self.properties = {
            "glucose_ratio": glucose_ratio,
            "white_cell_count": white_cell_count,
            "lactate_level": lactate_level
        }

    def diagnose(self):
        # Check the conditions for diagnosing bacterial meningitis
        if (self.properties["glucose_ratio"] <= 0.4 and 
            self.properties["white_cell_count"] >= 500 and 
            self.properties["lactate_level"] >= 31.53):
            return "Diagnosis: Positive for bacterial meningitis."
        else:
            return "Diagnosis: Not indicative of bacterial meningitis."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.diagnosis_result = self.rootObject.contains[0].diagnose()

    def _initialize_simulation(self):
        world = Container("environment")
        # Create a CSF analysis object with values that indicate a positive diagnosis
        csf_analysis = CSFAnalysis(glucose_ratio=0.4, white_cell_count=600, lactate_level=32)
        world.addObject(csf_analysis)
        return world

    def run(self):
        return self.diagnosis_result

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
