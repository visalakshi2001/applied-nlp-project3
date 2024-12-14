
# Claim: Noninvasive positive pressure ventilation is not predictive of acute respiratory failure after solid organ transplantation.
# The simulation will evaluate the effectiveness of Noninvasive Ventilation (NIV) compared to standard treatment in preventing acute respiratory failure.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, treatment_type, intubation_rate, improvement_rate):
        super().__init__(name)
        self.treatment_type = treatment_type
        self.intubation_rate = intubation_rate  # Percentage of patients requiring intubation
        self.improvement_rate = improvement_rate  # Percentage of patients showing improvement

    def makeDescriptionStr(self):
        return f"{self.name} treated with {self.treatment_type}: Intubation rate = {self.intubation_rate}%, Improvement rate = {self.improvement_rate}%."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("ICU")
        niv_patient = Patient("NIV Patient", "Noninvasive Ventilation", 20, 60)  # 20% intubation, 60% improvement
        standard_patient = Patient("Standard Patient", "Standard Treatment", 70, 25)  # 70% intubation, 25% improvement
        world.addObject(niv_patient)
        world.addObject(standard_patient)
        return world

    def evaluate_claim(self):
        niv_patient = self.rootObject.containsItemWithName("NIV Patient")[0]
        standard_patient = self.rootObject.containsItemWithName("Standard Patient")[0]

        if niv_patient.intubation_rate < standard_patient.intubation_rate:
            return "Claim Refuted: NIV is predictive of lower intubation rates."
        else:
            return "Claim Supported: NIV is not predictive of lower intubation rates."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.evaluate_claim()
    print(result)

if __name__ == "__main__":
    main()
