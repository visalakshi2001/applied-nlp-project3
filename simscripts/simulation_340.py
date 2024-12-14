
# Claim: Diabetes remission occurs less in people treated with conventional therapy than in people treated with laparoscopic adjustable gastric banding surgery.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, treatment_type, remission_rate=0):
        super().__init__(name)
        self.treatment_type = treatment_type
        self.remission_rate = remission_rate

    def calculate_remission(self):
        if self.treatment_type == "surgical":
            self.remission_rate = 73  # 73% remission for surgical group
        elif self.treatment_type == "conventional":
            self.remission_rate = 13  # 13% remission for conventional group

    def makeDescriptionStr(self):
        return f"{self.name} is treated with {self.treatment_type} therapy and has a remission rate of {self.remission_rate}%."

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.results = self._evaluate_remission()

    def _initialize_simulation(self):
        surgical_patient = Patient("Surgical Patient", "surgical")
        conventional_patient = Patient("Conventional Patient", "conventional")
        
        surgical_patient.calculate_remission()
        conventional_patient.calculate_remission()
        
        return [surgical_patient, conventional_patient]

    def _evaluate_remission(self):
        surgical_remission = self.patients[0].remission_rate
        conventional_remission = self.patients[1].remission_rate
        
        if surgical_remission > conventional_remission:
            return "Supported: Diabetes remission occurs less in people treated with conventional therapy."
        else:
            return "Refuted: Diabetes remission does not occur less in people treated with conventional therapy."

def main():
    simulation = Simulation()
    print(simulation.results)

if __name__ == "__main__":
    main()
