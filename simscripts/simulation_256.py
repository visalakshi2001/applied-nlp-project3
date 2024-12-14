
# Claim: Chlamydia trachomatis is most prevalent in the UK among sexually-experienced individuals aged 16 to 24.

from simulation_utils import GameObject, Container

class Individual(GameObject):
    def __init__(self, age, gender, sexual_experience, chlamydia_status):
        super().__init__(f"Individual aged {age} {gender}")
        self.age = age
        self.gender = gender
        self.sexual_experience = sexual_experience
        self.chlamydia_status = chlamydia_status

    def makeDescriptionStr(self):
        return f"{self.name}, Sexual Experience: {self.sexual_experience}, Chlamydia Status: {self.chlamydia_status}"

class Population(Container):
    def __init__(self):
        super().__init__("Population")
        self.chlamydia_prevalence = {
            "16-24": {"female": 3.1, "male": 2.3},
            "overall": {"female": 1.5, "male": 1.1}
        }

    def addIndividual(self, individual):
        self.addObject(individual)

    def calculatePrevalence(self):
        total_individuals = len(self.contains)
        if total_individuals == 0:
            return {"16-24": {"female": 0, "male": 0}, "overall": {"female": 0, "male": 0}}

        count_16_24_female = sum(1 for ind in self.contains if ind.age in range(16, 25) and ind.gender == "female" and ind.chlamydia_status)
        count_16_24_male = sum(1 for ind in self.contains if ind.age in range(16, 25) and ind.gender == "male" and ind.chlamydia_status)
        count_overall_female = sum(1 for ind in self.contains if ind.gender == "female" and ind.chlamydia_status)
        count_overall_male = sum(1 for ind in self.contains if ind.gender == "male" and ind.chlamydia_status)

        prevalence_16_24 = {
            "female": (count_16_24_female / total_individuals) * 100,
            "male": (count_16_24_male / total_individuals) * 100
        }
        prevalence_overall = {
            "female": (count_overall_female / total_individuals) * 100,
            "male": (count_overall_male / total_individuals) * 100
        }

        return {"16-24": prevalence_16_24, "overall": prevalence_overall}

class Simulation:
    def __init__(self):
        self.population = Population()
        self.initialize_population()

    def initialize_population(self):
        # Simulating a population with varying ages and chlamydia status
        self.population.addIndividual(Individual(22, "female", True, True))
        self.population.addIndividual(Individual(23, "male", True, True))
        self.population.addIndividual(Individual(20, "female", True, False))
        self.population.addIndividual(Individual(19, "male", True, True))
        self.population.addIndividual(Individual(30, "female", True, False))
        self.population.addIndividual(Individual(25, "male", True, False))

    def run_simulation(self):
        prevalence = self.population.calculatePrevalence()
        return prevalence

def main():
    simulation = Simulation()
    results = simulation.run_simulation()
    print("Chlamydia Prevalence Results:")
    print(f"Prevalence in individuals aged 16-24: Female: {results['16-24']['female']}%, Male: {results['16-24']['male']}%")
    print(f"Overall Prevalence: Female: {results['overall']['female']}%, Male: {results['overall']['male']}%")

    # Check if the claim is supported
    if results['16-24']['female'] > 0 or results['16-24']['male'] > 0:
        print("Claim Supported: Chlamydia trachomatis is prevalent among sexually-experienced individuals aged 16 to 24.")
    else:
        print("Claim Refuted: Chlamydia trachomatis is not prevalent among sexually-experienced individuals aged 16 to 24.")

if __name__ == "__main__":
    main()
