
# Claim: Patients with common epithelial cancers are more likely to have an emergency event as their first hospital admission if they live in resource-deprived areas.
# The simulation will model patients with different socioeconomic statuses and their likelihood of emergency admissions.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, cancer_type, is_deprived_area):
        super().__init__(name)
        self.cancer_type = cancer_type
        self.is_deprived_area = is_deprived_area
        self.emergency_admission = False

    def determine_admission(self):
        # Simulate the likelihood of emergency admission based on deprivation status
        if self.is_deprived_area:
            # Higher likelihood of emergency admission
            self.emergency_admission = True  # Simplified assumption for simulation
        else:
            self.emergency_admission = False  # Simplified assumption for simulation

    def makeDescriptionStr(self):
        admission_status = "emergency" if self.emergency_admission else "elective"
        return f"{self.name} with {self.cancer_type} cancer is admitted as {admission_status}."

class Hospital(Container):
    def __init__(self):
        super().__init__("Hospital")
        self.patients = []

    def add_patient(self, patient):
        self.addObject(patient)
        self.patients.append(patient)

    def simulate_admissions(self):
        for patient in self.patients:
            patient.determine_admission()

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see:\n"
        for patient in self.patients:
            outStr += "\t" + patient.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.hospital = Hospital()
        self.initialize_patients()
        self.hospital.simulate_admissions()
        self.observationStr = self.hospital.makeDescriptionStr()

    def initialize_patients(self):
        # Create patients with different cancer types and deprivation status
        self.hospital.add_patient(Patient("Patient 1", "breast", True))  # Deprived area
        self.hospital.add_patient(Patient("Patient 2", "lung", False))   # Not deprived area
        self.hospital.add_patient(Patient("Patient 3", "colorectal", True))  # Deprived area
        self.hospital.add_patient(Patient("Patient 4", "breast", False))  # Not deprived area

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
