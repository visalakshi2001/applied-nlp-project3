
# Claim: Risedronate increases risk of vertebral and non-vertebral fractures.
# The simulation will test the effects of Risedronate on fracture incidence.

from simulation_utils import GameObject, Container

class Risedronate(GameObject):
    def __init__(self, dosage):
        super().__init__("Risedronate")
        self.dosage = dosage
        self.properties = {
            "vertebral_fracture_incidence": 16.3,  # incidence in placebo group
            "non_vertebral_fracture_incidence": 8.4  # incidence in placebo group
        }

    def apply_treatment(self):
        if self.dosage == 5:
            # Decrease the incidence of fractures based on the study results
            self.properties["vertebral_fracture_incidence"] *= 0.59  # 41% reduction
            self.properties["non_vertebral_fracture_incidence"] *= 0.61  # 39% reduction

    def makeDescriptionStr(self):
        description = (f"Risedronate at {self.dosage} mg/d results in:\n"
                       f"Vertebral fracture incidence: {self.properties['vertebral_fracture_incidence']:.2f}%\n"
                       f"Non-vertebral fracture incidence: {self.properties['non_vertebral_fracture_incidence']:.2f}%")
        return description

class Simulation:
    def __init__(self):
        self.risedronate = Risedronate(dosage=5)  # Testing with 5 mg/d
        self.risedronate.apply_treatment()  # Apply treatment to see effects

    def run(self):
        return self.risedronate.makeDescriptionStr()

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

    # Determine if the claim is supported or refuted
    if (simulation.risedronate.properties["vertebral_fracture_incidence"] < 16.3 and
        simulation.risedronate.properties["non_vertebral_fracture_incidence"] < 8.4):
        print("Claim Supported: Risedronate decreases the risk of vertebral and non-vertebral fractures.")
    else:
        print("Claim Refuted: Risedronate does not increase the risk of vertebral and non-vertebral fractures.")

if __name__ == "__main__":
    main()
