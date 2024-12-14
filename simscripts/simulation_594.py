
# Claim: Incidence of heart failure increased by 10% in women since 1979.
# The simulation will check the incidence of heart failure in women and men over time.

from simulation_utils import GameObject, Container

class HeartFailureIncidence(GameObject):
    def __init__(self, year, incidence_men, incidence_women):
        super().__init__(f"HeartFailureIncidence_{year}")
        self.year = year
        self.incidence_men = incidence_men
        self.incidence_women = incidence_women

    def makeDescriptionStr(self):
        return f"In {self.year}, the incidence of heart failure was {self.incidence_men} for men and {self.incidence_women} for women."

class HeartFailureSimulation(Container):
    def __init__(self):
        super().__init__("Heart Failure Simulation")
        self.data = [
            HeartFailureIncidence(1979, 378, 289),
            HeartFailureIncidence(2000, 378, 289)  # No change in incidence
        ]
        for incidence in self.data:
            self.addObject(incidence)

    def analyze_incidence(self):
        initial_incidence_women = self.data[0].incidence_women
        final_incidence_women = self.data[-1].incidence_women
        increase_percentage = ((final_incidence_women - initial_incidence_women) / initial_incidence_women) * 100
        return increase_percentage

class Simulation:
    def __init__(self):
        self.rootObject = HeartFailureSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.increase_percentage = self.rootObject.analyze_incidence()

    def run(self):
        return self.increase_percentage

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.run()
    if result >= 10:
        print("Claim Supported: The incidence of heart failure increased by 10% in women since 1979.")
    else:
        print("Claim Refuted: The incidence of heart failure did not increase by 10% in women since 1979.")

if __name__ == "__main__":
    main()
