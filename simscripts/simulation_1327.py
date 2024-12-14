
# Claim: Tuberculosis incidence occurs at higher rates in more sparsely populated areas in the UK.
# The simulation will analyze the relationship between population density and tuberculosis incidence.

from simulation_utils import GameObject, Container

class PopulationDensity(GameObject):
    def __init__(self, name, density, tb_incidence):
        super().__init__(name)
        self.density = density  # Population density
        self.tb_incidence = tb_incidence  # Tuberculosis incidence rate

    def makeDescriptionStr(self):
        return f"{self.name} has a population density of {self.density} and a TB incidence rate of {self.tb_incidence}."

class TBIncidenceSimulation(Container):
    def __init__(self):
        super().__init__("TB Incidence Simulation")
        self.districts = []

    def addDistrict(self, name, density, tb_incidence):
        district = PopulationDensity(name, density, tb_incidence)
        self.addObject(district)
        self.districts.append(district)

    def analyze(self):
        # Analyze the relationship between population density and TB incidence
        high_density_tb = [d for d in self.districts if d.density > 1000]  # Arbitrary threshold for high density
        low_density_tb = [d for d in self.districts if d.density <= 1000]  # Low density

        high_density_incidence = sum(d.tb_incidence for d in high_density_tb) / len(high_density_tb) if high_density_tb else 0
        low_density_incidence = sum(d.tb_incidence for d in low_density_tb) / len(low_density_tb) if low_density_tb else 0

        return high_density_incidence, low_density_incidence

def main():
    simulation = TBIncidenceSimulation()
    
    # Adding districts with varying population densities and TB incidence rates
    simulation.addDistrict("District A", 1200, 50)  # High density
    simulation.addDistrict("District B", 800, 30)   # Low density
    simulation.addDistrict("District C", 1500, 70)  # High density
    simulation.addDistrict("District D", 600, 20)   # Low density
    simulation.addDistrict("District E", 300, 10)   # Low density

    high_incidence, low_incidence = simulation.analyze()

    # Determine if the claim is supported or refuted
    if low_incidence < high_incidence:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"High Density TB Incidence: {high_incidence}")
    print(f"Low Density TB Incidence: {low_incidence}")
    print(f"Claim Verification Result: {result}")

if __name__ == "__main__":
    main()
