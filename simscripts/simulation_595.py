
# Claim: Incidence of sepsis has fallen substantially from 2009 to 2014.
# The simulation will analyze the incidence of sepsis over the specified years based on clinical data.

from simulation_utils import GameObject, Container

class SepsisIncidence(GameObject):
    def __init__(self, year, incidence_rate):
        super().__init__(f"Sepsis Incidence in {year}")
        self.year = year
        self.incidence_rate = incidence_rate

    def makeDescriptionStr(self):
        return f"In {self.year}, the incidence rate of sepsis was {self.incidence_rate}%."

class SepsisSimulation(Container):
    def __init__(self):
        super().__init__("Sepsis Incidence Simulation")
        self.years = [2009, 2010, 2011, 2012, 2013, 2014]
        self.incidence_rates = [6.0, 6.0, 6.0, 6.0, 6.0, 6.0]  # Stable incidence rates based on the reference text
        self.create_sepsis_cases()

    def create_sepsis_cases(self):
        for year, rate in zip(self.years, self.incidence_rates):
            sepsis_case = SepsisIncidence(year, rate)
            self.addObject(sepsis_case)

    def analyze_trend(self):
        # Analyze the trend of sepsis incidence from 2009 to 2014
        initial_rate = self.contains[0].incidence_rate  # 2009
        final_rate = self.contains[-1].incidence_rate  # 2014
        if initial_rate == final_rate:
            return "The incidence of sepsis remained stable from 2009 to 2014."
        elif final_rate < initial_rate:
            return "The incidence of sepsis has fallen from 2009 to 2014."
        else:
            return "The incidence of sepsis has increased from 2009 to 2014."

class Simulation:
    def __init__(self):
        self.rootObject = SepsisSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.rootObject.analyze_trend()

    def run(self):
        return self.result

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.run())

if __name__ == "__main__":
    main()
