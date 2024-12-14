
# Claim: Walking in traffic areas in London did not improve lung function in elderly adults.
# The simulation will assess the lung function changes in elderly adults after walking in a polluted area versus a clean area.

from simulation_utils import GameObject, Container

class ElderlyAdult(GameObject):
    def __init__(self, name, lung_function=100):
        super().__init__(name)
        self.lung_function = lung_function  # Initial lung function score

    def walk_in_area(self, pollution_level):
        if pollution_level == "high":
            # Decrease lung function due to high pollution
            self.lung_function -= 10  # Arbitrary decrease for high pollution
        elif pollution_level == "low":
            # Increase lung function due to low pollution
            self.lung_function += 5  # Arbitrary increase for low pollution

    def makeDescriptionStr(self):
        return f"{self.name} has a lung function score of {self.lung_function}."

class Simulation:
    def __init__(self):
        self.adult_oxford = ElderlyAdult("Elderly Adult on Oxford Street")
        self.adult_hyde = ElderlyAdult("Elderly Adult in Hyde Park")
        self.run_simulation()

    def run_simulation(self):
        # Simulate walking in high pollution area (Oxford Street)
        self.adult_oxford.walk_in_area("high")
        # Simulate walking in low pollution area (Hyde Park)
        self.adult_hyde.walk_in_area("low")

    def results(self):
        return (self.adult_oxford.makeDescriptionStr(), self.adult_hyde.makeDescriptionStr())

def main():
    simulation = Simulation()
    oxford_result, hyde_result = simulation.results()
    print(oxford_result)
    print(hyde_result)

    # Determine if the claim is supported or refuted
    if simulation.adult_oxford.lung_function < 100 and simulation.adult_hyde.lung_function > 100:
        print("Claim is Refuted: Walking in traffic areas in London did not improve lung function in elderly adults.")
    else:
        print("Claim is Supported: Walking in traffic areas in London did not improve lung function in elderly adults.")

if __name__ == "__main__":
    main()
