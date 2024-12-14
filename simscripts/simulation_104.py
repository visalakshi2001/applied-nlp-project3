
# Claim: Allogeneic mechanical circulatory support is not as effective as autologous mechanical circulatory support for treating acute myocardial infarction.
# The simulation will compare the safety and efficacy of allogeneic and autologous MSC therapies based on the provided reference text.

from simulation_utils import GameObject, Container

class MSC(GameObject):
    def __init__(self, name, type, saes_rate, eef_change):
        super().__init__(name)
        self.type = type  # 'allogeneic' or 'autologous'
        self.properties = {
            "saes_rate": saes_rate,  # Serious Adverse Events rate
            "eef_change": eef_change   # Change in Ejection Fraction
        }

    def makeDescriptionStr(self):
        description = f"{self.type.capitalize()} MSC with SAEs rate of {self.properties['saes_rate']} and EEF change of {self.properties['eef_change']}."
        return description

class Patient(Container):
    def __init__(self, name):
        super().__init__(name)
        self.properties["isPatient"] = True

    def makeDescriptionStr(self):
        outStr = f"In the patient {self.name}, you have:\n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.compare_msc_effectiveness()

    def _initialize_simulation(self):
        patient = Patient("Patient_1")
        allogeneic_msc = MSC("Allogeneic_MSC", "allogeneic", 33.3, 0)  # 33.3% SAEs, no change in EEF
        autologous_msc = MSC("Autologous_MSC", "autologous", 53.3, 0)  # 53.3% SAEs, no change in EEF
        patient.addObject(allogeneic_msc)
        patient.addObject(autologous_msc)
        return patient

    def compare_msc_effectiveness(self):
        allogeneic_sae = self.rootObject.contains[0].properties["saes_rate"]
        autologous_sae = self.rootObject.contains[1].properties["saes_rate"]

        if allogeneic_sae < autologous_sae:
            self.result = "Supported: Allogeneic MSCs have a lower SAE rate than autologous MSCs."
        else:
            self.result = "Refuted: Allogeneic MSCs do not have a lower SAE rate than autologous MSCs."

    def makeDescriptionStr(self):
        return self.observationStr + "\n" + self.result

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
