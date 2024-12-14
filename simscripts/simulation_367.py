
# Claim: Early patent ductus arteriosus (PDA) screening decreases in-hospital mortality.
# The simulation will evaluate the effect of early screening on in-hospital mortality rates.

from simulation_utils import GameObject, Container

class Infant(GameObject):
    def __init__(self, name, screened=False):
        super().__init__(name)
        self.screened = screened
        self.mortality_rate = 0.185  # Default mortality rate for unscreened infants
        if screened:
            self.mortality_rate = 0.142  # Mortality rate for screened infants

    def makeDescriptionStr(self):
        return f"{self.name} (Screened: {self.screened}, Mortality Rate: {self.mortality_rate})"

class Hospital(Container):
    def __init__(self):
        super().__init__("Hospital")
        self.infants = []

    def add_infant(self, infant):
        self.addObject(infant)
        self.infants.append(infant)

    def calculate_mortality(self):
        total_infants = len(self.infants)
        if total_infants == 0:
            return 0
        total_mortality = sum(infant.mortality_rate for infant in self.infants)
        return total_mortality / total_infants

class Simulation:
    def __init__(self):
        self.hospital = Hospital()
        self.setup_infants()
        self.mortality_rate = self.hospital.calculate_mortality()

    def setup_infants(self):
        # Adding infants to the hospital, some screened and some not
        for i in range(847):  # Screened infants
            self.hospital.add_infant(Infant(f"Infant {i+1}", screened=True))
        for i in range(666):  # Not screened infants
            self.hospital.add_infant(Infant(f"Infant {i+1 + 847}"))

    def run_simulation(self):
        return self.mortality_rate

def main():
    simulation = Simulation()
    mortality_rate = simulation.run_simulation()
    print(f"Calculated In-Hospital Mortality Rate: {mortality_rate:.3f}")

    # Determine if the claim is supported or refuted
    if mortality_rate < 0.185:  # Compare with the mortality rate of unscreened infants
        print("Claim Supported: Early PDA screening decreases in-hospital mortality.")
    else:
        print("Claim Refuted: Early PDA screening does not decrease in-hospital mortality.")

if __name__ == "__main__":
    main()
