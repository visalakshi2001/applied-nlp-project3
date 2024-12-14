
# Claim: Exposure to fine particulate air pollution is unrelated to anxiety prevalence.
# The simulation will test the relationship between exposure to PM2.5 and anxiety symptoms.

from simulation_utils import GameObject, Container

class AirPollution(GameObject):
    def __init__(self, name, pm25_exposure=0):
        super().__init__(name)
        self.pm25_exposure = pm25_exposure
        self.anxiety_symptoms = 0

    def tick(self):
        # Simulate the effect of PM2.5 exposure on anxiety symptoms
        if self.pm25_exposure > 0:
            self.anxiety_symptoms = 1.12 * self.pm25_exposure  # Simplified relationship based on odds ratio
        else:
            self.anxiety_symptoms = 0

    def makeDescriptionStr(self):
        return f"{self.name} has PM2.5 exposure of {self.pm25_exposure} and anxiety symptoms score of {self.anxiety_symptoms}."

class Population(Container):
    def __init__(self):
        super().__init__("Population")
        self.properties["anxiety_prevalence"] = 0

    def calculate_anxiety_prevalence(self):
        total_symptoms = sum([obj.anxiety_symptoms for obj in self.contains])
        self.properties["anxiety_prevalence"] = total_symptoms / len(self.contains) if self.contains else 0

    def makeDescriptionStr(self):
        self.calculate_anxiety_prevalence()
        return f"In the {self.name}, the anxiety prevalence is {self.properties['anxiety_prevalence']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        population = Population()
        # Simulating 10 individuals with varying PM2.5 exposure
        for i in range(10):
            exposure = i * 5  # PM2.5 exposure increases with each individual
            individual = AirPollution(f"Individual_{i+1}", pm25_exposure=exposure)
            population.addObject(individual)
        return population

    def step(self):
        # Update the simulation
        self.rootObject.calculate_anxiety_prevalence()
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.step()
    print(result)

    # Determine if the claim is supported or refuted
    if simulation.rootObject.properties["anxiety_prevalence"] > 0:
        print("Claim is Refuted: Exposure to fine particulate air pollution is related to anxiety prevalence.")
    else:
        print("Claim is Supported: Exposure to fine particulate air pollution is unrelated to anxiety prevalence.")

if __name__ == "__main__":
    main()
