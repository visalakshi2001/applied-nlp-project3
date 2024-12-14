
# Claim: Ultrasound guidance significantly reduces the number of traumatic procedures when attempting needle insertion.
# The simulation will compare the number of traumatic procedures in ultrasound-guided vs. standard methods.

from simulation_utils import GameObject, Container

class Procedure(GameObject):
    def __init__(self, name, ultrasound_guided=False):
        super().__init__(name)
        self.ultrasound_guided = ultrasound_guided
        self.successful_attempts = 0
        self.traumatic_attempts = 0

    def perform_procedure(self):
        if self.ultrasound_guided:
            # Reduced risk of traumatic procedures
            self.traumatic_attempts = 1 if random.random() < 0.27 else 0  # 0.27 risk ratio
        else:
            self.traumatic_attempts = 1 if random.random() < 0.44 else 0  # 0.44 risk ratio (assumed for control)
        
        self.successful_attempts = 1 - self.traumatic_attempts

class Simulation:
    def __init__(self):
        self.ultrasound_procedure = Procedure("Ultrasound Guided Procedure", ultrasound_guided=True)
        self.standard_procedure = Procedure("Standard Procedure", ultrasound_guided=False)
        self.ultrasound_procedure.perform_procedure()
        self.standard_procedure.perform_procedure()

    def evaluate_claim(self):
        if self.ultrasound_procedure.traumatic_attempts < self.standard_procedure.traumatic_attempts:
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    result = simulation.evaluate_claim()
    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
