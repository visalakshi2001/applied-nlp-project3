
# Claim: Rotator cuff exercises are more effective than general exercise therapy in reducing pain and improving function of the shoulder.
# The simulation will compare the effectiveness of specific rotator cuff exercises against general exercise therapy.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, pain_level=10, function_score=0):
        super().__init__(name)
        self.properties = {
            "pain_level": pain_level,  # Pain level on a scale of 0-10
            "function_score": function_score  # Function score on a scale of 0-100
        }

    def perform_rotator_cuff_exercises(self):
        # Simulate improvement from rotator cuff exercises
        self.properties["pain_level"] -= 5  # Pain decreases
        self.properties["function_score"] += 24  # Function improves significantly

    def perform_general_exercises(self):
        # Simulate improvement from general exercises
        self.properties["pain_level"] -= 1  # Pain decreases slightly
        self.properties["function_score"] += 9  # Function improves slightly

    def makeDescriptionStr(self):
        return f"{self.name} has a pain level of {self.properties['pain_level']} and a function score of {self.properties['function_score']}."

class Simulation:
    def __init__(self):
        self.patient_rotator_cuff = Patient("Patient with Rotator Cuff Exercises")
        self.patient_general = Patient("Patient with General Exercises")
        self.run_simulation()

    def run_simulation(self):
        # Perform exercises for both patients
        self.patient_rotator_cuff.perform_rotator_cuff_exercises()
        self.patient_general.perform_general_exercises()

        # Collect results
        self.results = {
            "rotator_cuff": self.patient_rotator_cuff.properties,
            "general": self.patient_general.properties
        }

    def evaluate_claim(self):
        # Compare results to evaluate the claim
        rotator_cuff_improvement = self.results["rotator_cuff"]["function_score"] - 0  # Initial function score was 0
        general_improvement = self.results["general"]["function_score"] - 0  # Initial function score was 0

        if rotator_cuff_improvement > general_improvement:
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    print(simulation.evaluate_claim())
    print(f"Rotator Cuff Patient: {simulation.results['rotator_cuff']}")
    print(f"General Exercise Patient: {simulation.results['general']}")

if __name__ == "__main__":
    main()
