
# Claim: Upon viral challenge, influenza-specific memory CD4+ T cells greatly enhance the early production of inflammatory chemokines in the lung.

from simulation_utils import GameObject, Container

class MemoryCD4TCell(GameObject):
    def __init__(self, name, is_memory=True):
        super().__init__(name)
        self.is_memory = is_memory
        self.properties = {
            "inflammatory_chemokines": 0
        }

    def enhanceChemokineProduction(self):
        if self.is_memory:
            self.properties["inflammatory_chemokines"] += 10  # Arbitrary enhancement value
        else:
            self.properties["inflammatory_chemokines"] += 0

    def makeDescriptionStr(self):
        return f"A {self.name} with inflammatory chemokines level: {self.properties['inflammatory_chemokines']}."

class Lung(Container):
    def __init__(self):
        super().__init__("lung")
        self.memory_cd4_t_cells = []

    def addMemoryCD4TCell(self, t_cell):
        self.memory_cd4_t_cells.append(t_cell)
        self.addObject(t_cell)

    def simulateViralChallenge(self):
        for t_cell in self.memory_cd4_t_cells:
            t_cell.enhanceChemokineProduction()

    def makeDescriptionStr(self):
        outStr = super().makeDescriptionStr()
        outStr += "In the lung, you see:\n"
        for t_cell in self.memory_cd4_t_cells:
            outStr += "\t" + t_cell.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.lung = Lung()
        self.setupSimulation()

    def setupSimulation(self):
        # Adding memory CD4+ T cells
        memory_t_cell = MemoryCD4TCell("memory_CD4_T_cell_1")
        self.lung.addMemoryCD4TCell(memory_t_cell)

        # Simulate viral challenge
        self.lung.simulateViralChallenge()

    def run(self):
        return self.lung.makeDescriptionStr()

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
