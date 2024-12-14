
# Claim: Prescribed exercise training improves quality of life.
# The simulation will test the effects of exercise training on health status among patients with heart failure.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, exercise_training=False, health_status=0):
        super().__init__(name)
        self.exercise_training = exercise_training
        self.health_status = health_status

    def apply_exercise_training(self):
        if self.exercise_training:
            self.health_status += 5.21  # Improvement in health status due to exercise training
        else:
            self.health_status += 3.28  # Improvement in health status without exercise training

    def makeDescriptionStr(self):
        return f"{self.name} has a health status score of {self.health_status}."

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.results = self.run_simulation()

    def _initialize_simulation(self):
        patient_with_training = Patient("Patient A", exercise_training=True)
        patient_without_training = Patient("Patient B", exercise_training=False)
        return [patient_with_training, patient_without_training]

    def run_simulation(self):
        for patient in self.patients:
            patient.apply_exercise_training()
        return {patient.name: patient.health_status for patient in self.patients}

def main():
    simulation = Simulation()
    print("Simulation Results:")
    for patient, health_status in simulation.results.items():
        print(f"{patient}: Health Status = {health_status}")

    # Determine if the claim is supported or refuted
    if simulation.results["Patient A"] > simulation.results["Patient B"]:
        print("Claim Supported: Prescribed exercise training improves quality of life.")
    else:
        print("Claim Refuted: Prescribed exercise training does not improve quality of life.")

if __name__ == "__main__":
    main()
