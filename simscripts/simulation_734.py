
# Claim: MEK inhibitors are effective treatments in RAS-driven mouse models of cancer.
# The simulation will model the interaction between a MEK inhibitor and a RAS-driven cancer model.

from simulation_utils import GameObject, Container

class CancerModel(GameObject):
    def __init__(self, name, response_to_mechanism=0):
        super().__init__(name)
        self.properties = {
            "response_to_mechanism": response_to_mechanism  # 0 means no response, 1 means response
        }

    def apply_mechanism(self, mechanism):
        if mechanism == "MEK inhibitor":
            self.properties["response_to_mechanism"] = 1  # Indicate a positive response to MEK inhibitor

    def makeDescriptionStr(self):
        response = "no response" if self.properties["response_to_mechanism"] == 0 else "marked response"
        return f"A {self.name} model, which shows {response} to treatment."

class MEKInhibitor(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def apply_to(self, cancer_model):
        cancer_model.apply_mechanism(self.name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("environment")
        kras_cancer = CancerModel("Kras-driven lung cancer")
        mek_inhibitor = MEKInhibitor("MEK inhibitor")
        
        world.addObject(kras_cancer)
        world.addObject(mek_inhibitor)

        # Simulate applying the MEK inhibitor to the cancer model
        mek_inhibitor.apply_to(kras_cancer)
        
        return world

    def makeDescriptionStr(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
