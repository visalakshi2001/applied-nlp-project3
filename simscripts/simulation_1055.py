
# Claim: Risk-adjusted mortality rates are similar in teaching and non-teaching hospitals.
# The simulation will evaluate the risk-adjusted mortality rates based on the provided reference text.

from simulation_utils import GameObject, Container

class Hospital(GameObject):
    def __init__(self, name, teaching_status, mortality_rate):
        super().__init__(name)
        self.teaching_status = teaching_status  # True for teaching, False for non-teaching
        self.mortality_rate = mortality_rate  # Risk-adjusted mortality rate

    def makeDescriptionStr(self):
        return f"{self.name} (Teaching: {self.teaching_status}, Mortality Rate: {self.mortality_rate})"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.evaluate_claim()

    def _initialize_simulation(self):
        world = Container("hospital_environment")
        teaching_hospital = Hospital("Teaching Hospital A", True, 0.96)  # Example mortality rate
        non_teaching_hospital = Hospital("Non-Teaching Hospital B", False, 1.04)  # Example mortality rate
        world.addObject(teaching_hospital)
        world.addObject(non_teaching_hospital)
        return world

    def evaluate_claim(self):
        teaching_mortality = self.rootObject.contains[0].mortality_rate
        non_teaching_mortality = self.rootObject.contains[1].mortality_rate
        
        # Compare mortality rates
        if abs(teaching_mortality - non_teaching_mortality) < 0.1:  # Allowing a small margin of error
            self.observationStr += "\nClaim Supported: Risk-adjusted mortality rates are similar."
        else:
            self.observationStr += "\nClaim Refuted: Risk-adjusted mortality rates are not similar."

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
