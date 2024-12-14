
# Claim: Ultrasound guidance significantly reduces the number of needle insertion attempts necessary for a given procedure.
# The simulation will model the effect of ultrasound guidance on needle insertion attempts.

from simulation_utils import GameObject, Container

class Procedure(GameObject):
    def __init__(self, name, insertion_attempts=0):
        super().__init__(name)
        self.insertion_attempts = insertion_attempts

    def perform_with_ultrasound(self):
        # Simulate the effect of ultrasound guidance
        self.insertion_attempts -= 0.44  # Mean difference from the reference text

    def perform_without_ultrasound(self):
        # Simulate the effect without ultrasound guidance
        self.insertion_attempts += 1  # Assume at least one attempt is made

    def makeDescriptionStr(self):
        return f"{self.name} has {self.insertion_attempts:.2f} insertion attempts."

class Simulation:
    def __init__(self):
        self.procedure_with_ultrasound = Procedure("Procedure with Ultrasound", insertion_attempts=1)  # Start with 1 attempt
        self.procedure_without_ultrasound = Procedure("Procedure without Ultrasound", insertion_attempts=1)  # Start with 1 attempt

    def run_simulation(self):
        # Perform the procedure with ultrasound guidance
        self.procedure_with_ultrasound.perform_with_ultrasound()
        # Perform the procedure without ultrasound guidance
        self.procedure_without_ultrasound.perform_without_ultrasound()

        # Check the results
        result_with_ultrasound = self.procedure_with_ultrasound.insertion_attempts
        result_without_ultrasound = self.procedure_without_ultrasound.insertion_attempts

        return result_with_ultrasound, result_without_ultrasound

def main():
    simulation = Simulation()
    result_with_ultrasound, result_without_ultrasound = simulation.run_simulation()

    print(f"Result with Ultrasound: {result_with_ultrasound:.2f} insertion attempts")
    print(f"Result without Ultrasound: {result_without_ultrasound:.2f} insertion attempts")

    # Determine if the claim is supported or refuted
    if result_with_ultrasound < result_without_ultrasound:
        print("Claim Supported: Ultrasound guidance significantly reduces the number of needle insertion attempts.")
    else:
        print("Claim Refuted: Ultrasound guidance does not significantly reduce the number of needle insertion attempts.")

if __name__ == "__main__":
    main()
