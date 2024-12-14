
# Claim: General exercise therapy is more effective than rotator cuff exercises in reducing pain and improving function of the shoulder.
# The simulation will compare the effectiveness of two exercise strategies: specific rotator cuff exercises and general exercise therapy.

from simulation_utils import GameObject, Container

class Exercise(GameObject):
    def __init__(self, name, improvement_score=0):
        super().__init__(name)
        self.improvement_score = improvement_score

    def perform_exercise(self):
        # Simulate the improvement in shoulder function and pain reduction
        if self.name == "Specific Rotator Cuff Exercises":
            self.improvement_score += 24  # Based on the study results
        elif self.name == "General Exercise Therapy":
            self.improvement_score += 9  # Control group score

    def makeDescriptionStr(self):
        return f"{self.name} has an improvement score of {self.improvement_score}."

class Simulation:
    def __init__(self):
        self.rotator_cuff_exercise = Exercise("Specific Rotator Cuff Exercises")
        self.general_exercise = Exercise("General Exercise Therapy")
        self.exercises = [self.rotator_cuff_exercise, self.general_exercise]

    def run_simulation(self):
        for exercise in self.exercises:
            exercise.perform_exercise()

    def evaluate_claim(self):
        self.run_simulation()
        rotator_cuff_score = self.rotator_cuff_exercise.improvement_score
        general_exercise_score = self.general_exercise.improvement_score
        
        if rotator_cuff_score > general_exercise_score:
            return "Claim Refuted: Specific rotator cuff exercises are more effective."
        else:
            return "Claim Supported: General exercise therapy is more effective."

def main():
    simulation = Simulation()
    result = simulation.evaluate_claim()
    print(result)

if __name__ == "__main__":
    main()
