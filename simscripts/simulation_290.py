
# Claim: Cost effectiveness evaluations based on cRCT data accurately reflect prices for patients in actual clinical practice.
# The simulation will evaluate the cost-effectiveness of coxibs based on RCT data versus actual clinical practice data.

from simulation_utils import GameObject, Container

class CostEffectivenessAnalysis(GameObject):
    def __init__(self, name, rct_cost, gprd_cost):
        super().__init__(name)
        self.properties = {
            "RCT_Cost": rct_cost,
            "GPRD_Cost": gprd_cost,
            "validity": None
        }

    def evaluate(self):
        # Compare RCT cost with GPRD cost to determine validity
        if self.properties["RCT_Cost"] > self.properties["GPRD_Cost"]:
            self.properties["validity"] = "Refuted"
        else:
            self.properties["validity"] = "Supported"

    def makeDescriptionStr(self):
        return f"{self.name}: RCT Cost = ${self.properties['RCT_Cost']}, GPRD Cost = ${self.properties['GPRD_Cost']}, Validity = {self.properties['validity']}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "Cost Effectiveness Analysis Environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_evaluation()

    def _initialize_simulation(self):
        world = World()
        # RCT costs from the reference text
        rct_cost_vigor = 16000  # VIGOR RCT cost
        rct_cost_class = 20000  # CLASS RCT cost
        # GPRD costs from the reference text
        gprd_cost = 58000  # GPRD cost during 1990-1993

        # Create cost-effectiveness analysis objects
        analysis_vigor = CostEffectivenessAnalysis("VIGOR Analysis", rct_cost_vigor, gprd_cost)
        analysis_class = CostEffectivenessAnalysis("CLASS Analysis", rct_cost_class, gprd_cost)

        world.addObject(analysis_vigor)
        world.addObject(analysis_class)
        return world

    def run_evaluation(self):
        # Evaluate each analysis
        for analysis in self.rootObject.contains:
            analysis.evaluate()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
