
# Claim: Mice that lack Interferon-γ or its receptor are highly susceptible to experimental autoimmune myocarditis.
# Simulation to verify the claim based on the provided reference text.

from simulation_utils import GameObject, Container

class Mouse(GameObject):
    def __init__(self, name, has_IFN_gamma_receptor=True):
        super().__init__(name)
        self.has_IFN_gamma_receptor = has_IFN_gamma_receptor
        self.properties = {
            "myocarditis_severity": 0,
            "mortality": 0
        }

    def develop_myocarditis(self):
        if not self.has_IFN_gamma_receptor:
            self.properties["myocarditis_severity"] = 10  # High severity for receptor-deficient mice
            self.properties["mortality"] = 1  # High mortality
        else:
            self.properties["myocarditis_severity"] = 2  # Low severity for wild-type mice
            self.properties["mortality"] = 0  # No mortality

    def makeDescriptionStr(self):
        description = f"A {self.name} mouse, with myocarditis severity {self.properties['myocarditis_severity']} and mortality {self.properties['mortality']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("environment")
        wild_type_mouse = Mouse("wild_type_mouse", has_IFN_gamma_receptor=True)
        ifn_gamma_deficient_mouse = Mouse("IFN_gamma_deficient_mouse", has_IFN_gamma_receptor=False)
        world.addObject(wild_type_mouse)
        world.addObject(ifn_gamma_deficient_mouse)
        return world

    def run_simulation(self):
        all_mice = self.rootObject.getAllContainedObjectsRecursive()
        for mouse in all_mice:
            mouse.develop_myocarditis()

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
