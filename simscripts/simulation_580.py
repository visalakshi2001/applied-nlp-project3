
# Claim: In pediatric tissue, most T cells are naive T cell emigrants from the thymus.
# The simulation will model T cell populations in pediatric and adult tissues to verify the claim.

from simulation_utils import GameObject, Container

class TCell(GameObject):
    def __init__(self, name, t_cell_type):
        super().__init__(name)
        self.properties = {
            "t_cell_type": t_cell_type  # Type of T cell: "naive", "memory", "effector_memory", "regulatory"
        }

    def makeDescriptionStr(self):
        return f"A {self.properties['t_cell_type']} T cell named {self.name}."

class Tissue(Container):
    def __init__(self, name):
        super().__init__(name)

    def countTCellsByType(self, t_cell_type):
        return sum(1 for cell in self.contains if cell.properties['t_cell_type'] == t_cell_type)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("world")
        
        # Create pediatric and adult tissues
        pediatric_tissue = Tissue("pediatric_tissue")
        adult_tissue = Tissue("adult_tissue")

        # Populate pediatric tissue with T cells
        for i in range(8):  # 8 naive T cells
            pediatric_tissue.addObject(TCell(f"naive_T_cell_{i+1}", "naive"))
        for i in range(2):  # 2 effector memory T cells
            pediatric_tissue.addObject(TCell(f"effector_memory_T_cell_{i+1}", "effector_memory"))
        for i in range(3):  # 3 regulatory T cells
            pediatric_tissue.addObject(TCell(f"regulatory_T_cell_{i+1}", "regulatory"))

        # Populate adult tissue with T cells
        for i in range(2):  # 2 naive T cells
            adult_tissue.addObject(TCell(f"naive_T_cell_{i+1}", "naive"))
        for i in range(6):  # 6 memory T cells
            adult_tissue.addObject(TCell(f"memory_T_cell_{i+1}", "memory"))

        world.addObject(pediatric_tissue)
        world.addObject(adult_tissue)
        return world

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

    def verifyClaim(self):
        pediatric_tissue = self.rootObject.contains[0]  # First object is pediatric tissue
        adult_tissue = self.rootObject.contains[1]      # Second object is adult tissue

        # Count T cells in pediatric tissue
        naive_count = pediatric_tissue.countTCellsByType("naive")
        effector_memory_count = pediatric_tissue.countTCellsByType("effector_memory")
        regulatory_count = pediatric_tissue.countTCellsByType("regulatory")

        # Count T cells in adult tissue
        memory_count = adult_tissue.countTCellsByType("memory")

        # Check if naive T cells are the majority in pediatric tissue
        total_pediatric_t_cells = naive_count + effector_memory_count + regulatory_count
        if total_pediatric_t_cells > 0 and naive_count > (effector_memory_count + regulatory_count):
            return "Supported: Most T cells in pediatric tissue are naive T cell emigrants from the thymus."
        else:
            return "Refuted: Most T cells in pediatric tissue are not naive T cell emigrants from the thymus."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.verifyClaim()
    print(result)

if __name__ == "__main__":
    main()
