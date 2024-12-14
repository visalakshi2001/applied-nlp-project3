
# Claim: Pediatric SCD patients with vaso-occlusive crisis show increased morphine use after breathing 80 ppm iNO for 4 hours.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, morphine_use=0, pain_score=0):
        super().__init__(name)
        self.properties = {
            "morphine_use": morphine_use,  # in mg/kg
            "pain_score": pain_score  # pain score on a scale
        }

    def inhale_iNO(self, duration_hours):
        # Simulate the effect of inhaling iNO for a certain duration
        if duration_hours == 4:
            # After 4 hours, morphine use does not significantly change
            self.properties["morphine_use"] += 0.32  # mg/kg for placebo
        elif duration_hours == 6:
            # After 6 hours, morphine use is significantly less
            self.properties["morphine_use"] += 0.29  # mg/kg for iNO

    def makeDescriptionStr(self):
        return f"{self.name} has used {self.properties['morphine_use']} mg/kg of morphine and has a pain score of {self.properties['pain_score']}."

class Simulation:
    def __init__(self):
        self.patient = Patient("Pediatric SCD Patient")
        self.run_simulation()

    def run_simulation(self):
        # Initial state before inhalation
        print(self.patient.makeDescriptionStr())
        
        # Inhale iNO for 4 hours
        self.patient.inhale_iNO(4)
        print("After inhaling iNO for 4 hours:")
        print(self.patient.makeDescriptionStr())

        # Inhale iNO for 6 hours to compare
        self.patient.inhale_iNO(6)
        print("After inhaling iNO for 6 hours:")
        print(self.patient.makeDescriptionStr())

def main():
    simulation = Simulation()

if __name__ == "__main__":
    main()
