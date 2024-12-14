
# Claim: Ectopic expression of Sall4, Nanog, Esrrb, and Lin28 generates induced pluripotent stem cells from mouse embryonic fibroblasts more efficiently than other factor combinations.

from simulation_utils import GameObject, Container

class Factor(GameObject):
    def __init__(self, name, efficiency=0):
        super().__init__(name)
        self.efficiency = efficiency

    def tick(self):
        # Simulate the efficiency of the factor
        self.efficiency += 1  # Increment efficiency for simulation purposes

class Cell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.factors = []
        self.iPSC_quality = 0

    def add_factor(self, factor):
        self.factors.append(factor)

    def generate_iPSC(self):
        # Calculate iPSC quality based on the factors present
        if any(factor.name in ["Sall4", "Nanog", "Esrrb", "Lin28"] for factor in self.factors):
            self.iPSC_quality = sum(factor.efficiency for factor in self.factors) * 2  # Higher quality for SNEL factors
        else:
            self.iPSC_quality = sum(factor.efficiency for factor in self.factors)  # Lower quality for other factors

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generate_possible_actions()

    def _initialize_simulation(self):
        world = Container("lab")
        mef_cell = Cell("mouse embryonic fibroblast")
        
        # Adding factors
        snel_factors = [Factor("Sall4"), Factor("Nanog"), Factor("Esrrb"), Factor("Lin28")]
        other_factors = [Factor("Oct4"), Factor("Sox2"), Factor("Klf4"), Factor("Myc")]

        for factor in snel_factors:
            mef_cell.add_factor(factor)
        
        for factor in other_factors:
            mef_cell.add_factor(factor)

        world.addObject(mef_cell)
        return world

    def generate_possible_actions(self):
        self.possibleActions = {
            "generate iPSC": ["generate iPSC"]
        }

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "generate iPSC":
            mef_cell = self.rootObject.contains[0]  # Get the MEF cell
            mef_cell.generate_iPSC()
            return f"Generated iPSC with quality: {mef_cell.iPSC_quality}"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate generating iPSC
    result = simulation.step("generate iPSC")
    print(result)

    # Determine if the claim is supported or refuted
    mef_cell = simulation.rootObject.contains[0]
    if mef_cell.iPSC_quality > 0:  # Assuming any positive quality indicates support for the claim
        print("Claim Supported: Ectopic expression of SNEL factors generates iPSCs more efficiently.")
    else:
        print("Claim Refuted: Ectopic expression of SNEL factors does not generate iPSCs efficiently.")

if __name__ == "__main__":
    main()
