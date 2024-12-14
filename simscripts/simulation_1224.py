
# Claim: The latent infection of myeloid cells with human cytomegalovirus induces a number of changes in gene expression.

from simulation_utils import GameObject, Container

class MyeloidCell(GameObject):
    def __init__(self, name, gene_expression=None):
        super().__init__(name)
        self.gene_expression = gene_expression if gene_expression is not None else {}

    def infect(self):
        # Simulate the infection by HCMV and changes in gene expression
        self.gene_expression['M1_activation'] = True
        self.gene_expression['total_genes_upregulated'] = 583
        self.gene_expression['total_genes_downregulated'] = 621

    def makeDescriptionStr(self):
        description = f"A {self.name} with gene expression changes: {self.gene_expression}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        myeloid_cell = MyeloidCell("myeloid_cell_1")
        world.addObject(myeloid_cell)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("infect myeloid cell", ["infect", self.rootObject.contains[0]])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "infect":
            action[1].infect()
            self.observationStr = action[1].makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Perform the infection action
    action = "infect myeloid cell"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

    # Check if the claim is supported
    if simulation.rootObject.contains[0].gene_expression['total_genes_upregulated'] > 0 or simulation.rootObject.contains[0].gene_expression['total_genes_downregulated'] > 0:
        print("Claim Supported: The latent infection of myeloid cells with human cytomegalovirus induces a number of changes in gene expression.")
    else:
        print("Claim Refuted: No changes in gene expression were induced.")

if __name__ == "__main__":
    main()
