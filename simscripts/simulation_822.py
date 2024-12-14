
# Claim: N348I mutations cause resistance to nevirapine.
# The simulation will model the effect of N348I mutations on nevirapine susceptibility.

from simulation_utils import GameObject, Container

class Virus(GameObject):
    def __init__(self, name, nevirapine_susceptibility=1.0):
        super().__init__(name)
        self.properties = {
            "nevirapine_susceptibility": nevirapine_susceptibility  # 1.0 means fully susceptible
        }

    def introduce_mutation(self, mutation_effect):
        self.properties["nevirapine_susceptibility"] *= mutation_effect

    def makeDescriptionStr(self):
        return f"A {self.name} with nevirapine susceptibility of {self.properties['nevirapine_susceptibility']}."

class Simulation:
    def __init__(self):
        self.virus = Virus("HIV-1")
        self.mutation_effect = 7.4  # N348I decreases susceptibility to nevirapine by 7.4-fold
        self.virus.introduce_mutation(self.mutation_effect)

    def run(self):
        return self.virus.makeDescriptionStr()

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

    # Determine if the claim is supported or refuted
    if simulation.virus.properties["nevirapine_susceptibility"] < 1.0:
        print("Claim Supported: N348I mutations cause resistance to nevirapine.")
    else:
        print("Claim Refuted: N348I mutations do not cause resistance to nevirapine.")

if __name__ == "__main__":
    main()
