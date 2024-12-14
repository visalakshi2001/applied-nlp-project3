
# Claim: Egr3 regulates the homeostasis of B and T cells.
# The simulation will model the effects of Egr3 on B and T cell function and homeostasis.

from simulation_utils import GameObject, Container

class Lymphocyte(GameObject):
    def __init__(self, name, egr3_active=True):
        super().__init__(name)
        self.egr3_active = egr3_active
        self.properties = {
            "proinflammatory_cytokines": 0,
            "antigen_receptor_proliferation": 1,  # 1 indicates normal proliferation
            "STAT1_activity": 1,  # 1 indicates normal activity
            "STAT3_activity": 1,  # 1 indicates normal activity
            "AP1_activity": 1  # 1 indicates normal activity
        }

    def tick(self):
        if not self.egr3_active:
            self.properties["proinflammatory_cytokines"] += 5  # Excessive cytokines
            self.properties["antigen_receptor_proliferation"] = 0  # Impaired proliferation
            self.properties["STAT1_activity"] = 2  # Hyperactive
            self.properties["STAT3_activity"] = 2  # Hyperactive
            self.properties["AP1_activity"] = 0  # Severely impaired
        else:
            self.properties["proinflammatory_cytokines"] = 0  # Normal
            self.properties["antigen_receptor_proliferation"] = 1  # Normal
            self.properties["STAT1_activity"] = 1  # Normal
            self.properties["STAT3_activity"] = 1  # Normal
            self.properties["AP1_activity"] = 1  # Normal

    def makeDescriptionStr(self):
        description = (f"A {self.name} with Egr3 {'active' if self.egr3_active else 'inactive'}, "
                       f"proinflammatory cytokines: {self.properties['proinflammatory_cytokines']}, "
                       f"antigen receptor proliferation: {self.properties['antigen_receptor_proliferation']}, "
                       f"STAT1 activity: {self.properties['STAT1_activity']}, "
                       f"STAT3 activity: {self.properties['STAT3_activity']}, "
                       f"AP-1 activity: {self.properties['AP1_activity']}.")
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "immune system")
        self.b_cells = Lymphocyte("B cell", egr3_active=False)  # Egr3 inactive
        self.t_cells = Lymphocyte("T cell", egr3_active=False)  # Egr3 inactive
        self.addObject(self.b_cells)
        self.addObject(self.t_cells)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        return world

    def run_simulation(self):
        # Simulate the effects of Egr3 on B and T cells
        self.rootObject.b_cells.tick()
        self.rootObject.t_cells.tick()

    def get_results(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.get_results())

if __name__ == "__main__":
    main()
