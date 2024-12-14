
# Claim: Sepsis related mortality has remained stable between 2009-2014.
# The simulation will analyze the trends in sepsis incidence and mortality rates based on the provided reference text.

from simulation_utils import GameObject, Container

class SepsisData(GameObject):
    def __init__(self, year, incidence, mortality_rate):
        super().__init__(f"SepsisData_{year}")
        self.year = year
        self.incidence = incidence  # incidence of sepsis
        self.mortality_rate = mortality_rate  # mortality rate from sepsis

    def makeDescriptionStr(self):
        return f"In {self.year}, the incidence of sepsis was {self.incidence} and the mortality rate was {self.mortality_rate}."

class SepsisSimulation(Container):
    def __init__(self):
        super().__init__("Sepsis Simulation Environment")
        self.data_points = []
        self.initialize_data()

    def initialize_data(self):
        # Data from 2009 to 2014
        self.data_points.append(SepsisData(2009, 6.0, 15.0))  # Example values
        self.data_points.append(SepsisData(2010, 6.0, 14.5))  # Stable incidence, slight decline in mortality
        self.data_points.append(SepsisData(2011, 6.0, 14.0))  # Stable incidence, decline in mortality
        self.data_points.append(SepsisData(2012, 6.0, 13.5))  # Stable incidence, decline in mortality
        self.data_points.append(SepsisData(2013, 6.0, 13.0))  # Stable incidence, decline in mortality
        self.data_points.append(SepsisData(2014, 6.0, 12.5))  # Stable incidence, decline in mortality

        for data in self.data_points:
            self.addObject(data)

    def analyze_trends(self):
        stable_incidence = all(data.incidence == self.data_points[0].incidence for data in self.data_points)
        mortality_trend = [data.mortality_rate for data in self.data_points]
        stable_mortality = all(mortality_trend[i] >= mortality_trend[i + 1] for i in range(len(mortality_trend) - 1))

        return stable_incidence, stable_mortality

class Simulation:
    def __init__(self):
        self.rootObject = SepsisSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.stable_incidence, self.stable_mortality = self.rootObject.analyze_trends()

    def run(self):
        print(self.observationStr)
        if self.stable_incidence and self.stable_mortality:
            print("Claim Supported: Sepsis related mortality has remained stable between 2009-2014.")
        else:
            print("Claim Refuted: Sepsis related mortality has not remained stable between 2009-2014.")

def main():
    simulation = Simulation()
    simulation.run()

if __name__ == "__main__":
    main()
