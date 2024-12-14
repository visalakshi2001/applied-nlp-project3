
# Claim: Mathematical models predict that using Artemisinin-based combination therapy over nongametocytocidal drugs have only a modest impact in reducing malaria transmission.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Treatment(GameObject):
    def __init__(self, name, gametocytocidal_effect=0, prophylactic_time=0):
        super().__init__(name)
        self.properties = {
            "gametocytocidal_effect": gametocytocidal_effect,
            "prophylactic_time": prophylactic_time
        }

    def makeDescriptionStr(self):
        description = f"{self.name} with gametocytocidal effect of {self.properties['gametocytocidal_effect']} and prophylactic time of {self.properties['prophylactic_time']}."
        return description

class MalariaSimulation(Container):
    def __init__(self):
        super().__init__("Malaria Treatment Simulation")
        self.addObject(Treatment("Artemisinin-based Combination Therapy", gametocytocidal_effect=0, prophylactic_time=1))  # Short-acting ACT
        self.addObject(Treatment("Nongametocytocidal Drug", gametocytocidal_effect=0, prophylactic_time=2))  # Long-acting drug

    def evaluate_treatments(self):
        act = self.containsItemWithName("Artemisinin-based Combination Therapy")[0]
        nongametocytocidal = self.containsItemWithName("Nongametocytocidal Drug")[0]

        # Simulating the impact on transmission
        if nongametocytocidal.properties["prophylactic_time"] > act.properties["prophylactic_time"]:
            return "Nongametocytocidal drugs are more effective at reducing transmission than Artemisinin-based combination therapy."
        else:
            return "Artemisinin-based combination therapy is more effective at reducing transmission."

# Running the simulation
def main():
    simulation = MalariaSimulation()
    print(simulation.makeDescriptionStr())
    result = simulation.evaluate_treatments()
    print(result)

    # Determining the claim's support or refutation
    if "more effective" in result:
        print("Claim is Refuted.")
    else:
        print("Claim is Supported.")

if __name__ == "__main__":
    main()
