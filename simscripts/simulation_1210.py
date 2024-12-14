
# Claim: The density of cytokine receptor bearing cells affects the distance over which cytokines act.
# This simulation will model the relationship between the density of cytokine receptor bearing cells and the distance of cytokine action.

from simulation_utils import GameObject, Container

class Cytokine(GameObject):
    def __init__(self, name, diffusion_rate=1.0):
        super().__init__(name)
        self.diffusion_rate = diffusion_rate  # Rate at which cytokines diffuse

class CytokineReceptorBearingCell(GameObject):
    def __init__(self, name, density=1):
        super().__init__(name)
        self.density = density  # Density of cytokine receptor bearing cells

class ImmuneResponseSimulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.calculate_cytokine_action_distance()

    def _initialize_simulation(self):
        world = Container("immune_environment")
        cytokine = Cytokine("cytokine_1", diffusion_rate=1.5)
        cell1 = CytokineReceptorBearingCell("cell_1", density=5)  # High density
        cell2 = CytokineReceptorBearingCell("cell_2", density=1)  # Low density
        world.addObject(cytokine)
        world.addObject(cell1)
        world.addObject(cell2)
        return world

    def calculate_cytokine_action_distance(self):
        # The distance over which cytokines act is inversely related to the density of receptor bearing cells
        # Higher density leads to shorter action distance due to consumption of cytokines
        cell1_density = self.rootObject.contains[1].density
        cell2_density = self.rootObject.contains[2].density
        
        # Assuming a simple model where distance is inversely proportional to density
        distance_cell1 = 100 / cell1_density  # Distance for high density cell
        distance_cell2 = 100 / cell2_density  # Distance for low density cell
        
        self.result = {
            "cell_1_distance": distance_cell1,
            "cell_2_distance": distance_cell2
        }

    def makeDescriptionStr(self):
        return f"In the simulation, cytokine action distances are:\nCell 1 (high density): {self.result['cell_1_distance']} µm\nCell 2 (low density): {self.result['cell_2_distance']} µm"

def main():
    simulation = ImmuneResponseSimulation()
    print(simulation.observationStr)
    if simulation.result['cell_1_distance'] < simulation.result['cell_2_distance']:
        print("Claim Supported: Higher density of cytokine receptor bearing cells results in shorter action distance for cytokines.")
    else:
        print("Claim Refuted: Higher density of cytokine receptor bearing cells does not result in shorter action distance for cytokines.")

if __name__ == "__main__":
    main()
