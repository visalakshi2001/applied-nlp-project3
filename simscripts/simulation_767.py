
# Claim: Men are more susceptible to death due to pneumonia when compared to women.
# The simulation will analyze the mortality rates of men and women due to pneumonia based on the provided reference text.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, gender, pneumonia_mortality_rate):
        super().__init__(name)
        self.gender = gender
        self.pneumonia_mortality_rate = pneumonia_mortality_rate

    def makeDescriptionStr(self):
        return f"{self.name} (Gender: {self.gender}, Pneumonia Mortality Rate: {self.pneumonia_mortality_rate}%)"

class Hospital(Container):
    def __init__(self):
        super().__init__("Hospital")
        self.patients = []

    def addPatient(self, patient):
        self.addObject(patient)
        self.patients.append(patient)

    def calculateMortalityRates(self):
        male_mortality = sum(p.pneumonia_mortality_rate for p in self.patients if p.gender == "male") / len([p for p in self.patients if p.gender == "male"])
        female_mortality = sum(p.pneumonia_mortality_rate for p in self.patients if p.gender == "female") / len([p for p in self.patients if p.gender == "female"])
        return male_mortality, female_mortality

class Simulation:
    def __init__(self):
        self.hospital = Hospital()
        self.setupPatients()
        self.male_mortality, self.female_mortality = self.hospital.calculateMortalityRates()

    def setupPatients(self):
        # Adding patients with their respective pneumonia mortality rates
        self.hospital.addPatient(Patient("Patient 1", "male", 18))
        self.hospital.addPatient(Patient("Patient 2", "female", 34))
        self.hospital.addPatient(Patient("Patient 3", "male", 18))
        self.hospital.addPatient(Patient("Patient 4", "female", 34))

    def runSimulation(self):
        return self.male_mortality, self.female_mortality

def main():
    simulation = Simulation()
    male_mortality, female_mortality = simulation.runSimulation()
    
    print(f"Average Pneumonia Mortality Rate for Males: {male_mortality}%")
    print(f"Average Pneumonia Mortality Rate for Females: {female_mortality}%")
    
    if male_mortality > female_mortality:
        print("Claim Supported: Men are more susceptible to death due to pneumonia compared to women.")
    else:
        print("Claim Refuted: Men are not more susceptible to death due to pneumonia compared to women.")

if __name__ == "__main__":
    main()
