
# Claim: The density of cytokine receptor bearing cells has no effect on the distance over which cytokines act.
# The simulation will test the relationship between the density of cytokine receptor bearing cells and the distance of cytokine action.

from simulation_utils import GameObject, Container

class Cytokine(GameObject):
    def __init__(self, name, diffusion_rate=1.0):
        super().__init__(name)
        self.diffusion_rate = diffusion_rate  # Rate at which cytokines diffuse
        self.concentration = 0  # Initial concentration of cytokines

    def tick(self):
        # Simulate diffusion of cytokines
        self.concentration += self.diffusion_rate

class CytokineReceptorBearingCell(GameObject):
    def __init__(self, name, density=1):
        super().__init__(name)
        self.density = density  # Density of cytokine receptor bearing cells

    def tick(self):
        # Simulate consumption of cytokines based on density
        self.consumed_cytokines = self.density * 0.1  # Arbitrary consumption rate based on density

class ImmuneEnvironment(Container):
    def __init__(self):
        super().__init__("immune environment")
        self.cytokine = Cytokine("cytokine")
        self.cell1 = CytokineReceptorBearingCell("cell_1", density=1)
        self.cell2 = CytokineReceptorBearingCell("cell_2", density=5)  # Higher density
        self.addObject(self.cytokine)
        self.addObject(self.cell1)
        self.addObject(self.cell2)

    def makeDescriptionStr(self):
        return f"In the {self.name}, there is a cytokine with concentration {self.cytokine.concentration} and two cells with densities {self.cell1.density} and {self.cell2.density}."

class CytokineSimulation:
    def __init__(self):
        self.rootObject = ImmuneEnvironment()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def step(self):
        # Simulate one time step
        self.rootObject.cytokine.tick()
        self.rootObject.cell1.tick()
        self.rootObject.cell2.tick()
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = CytokineSimulation()
    print(simulation.observationStr)

    # Simulate multiple steps to observe the effect of cell density on cytokine action
    for _ in range(5):
        obs = simulation.step()
        print(obs)

if __name__ == "__main__":
    main()
