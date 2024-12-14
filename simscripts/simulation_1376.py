
# Claim: Whole brain radiotherapy increases the occurrence of new brain metastases.
# The simulation will compare the brain tumor recurrence rates between two treatment groups.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, treatment, brain_metastases_rate):
        super().__init__(name)
        self.treatment = treatment  # Treatment type: "WBRT + SRS" or "SRS alone"
        self.brain_metastases_rate = brain_metastases_rate  # Rate of brain metastases

    def makeDescriptionStr(self):
        return f"{self.name} treated with {self.treatment} has a brain metastases rate of {self.brain_metastases_rate}%."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.compare_treatment_effects()

    def _initialize_simulation(self):
        world = Container("hospital")
        patient1 = Patient("Patient 1", "WBRT + SRS", 46.8)  # Brain metastases rate for WBRT + SRS
        patient2 = Patient("Patient 2", "SRS alone", 76.4)  # Brain metastases rate for SRS alone
        world.addObject(patient1)
        world.addObject(patient2)
        return world

    def compare_treatment_effects(self):
        # Compare the brain metastases rates
        wbtr_srs_rate = 46.8
        srs_alone_rate = 76.4

        if wbtr_srs_rate < srs_alone_rate:
            self.observationStr += "\nConclusion: Whole brain radiotherapy (WBRT) combined with SRS reduces the occurrence of new brain metastases compared to SRS alone."
            self.result = "Supported"
        else:
            self.observationStr += "\nConclusion: Whole brain radiotherapy (WBRT) does not reduce the occurrence of new brain metastases compared to SRS alone."
            self.result = "Refuted"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(f"Claim verification result: {simulation.result}")

if __name__ == "__main__":
    main()
