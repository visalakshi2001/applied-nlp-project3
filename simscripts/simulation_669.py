
# Claim: Klf4 is not required for proper myeloid cell differentiation.
# The simulation will test the role of Klf4 in myeloid cell differentiation based on the provided reference text.

from simulation_utils import GameObject, Container

class MyeloidCell(GameObject):
    def __init__(self, name, Klf4_present=True):
        super().__init__(name)
        self.Klf4_present = Klf4_present
        self.differentiation_status = "undifferentiated"

    def differentiate(self):
        if self.Klf4_present:
            self.differentiation_status = "properly differentiated"
        else:
            self.differentiation_status = "improperly differentiated"

    def makeDescriptionStr(self):
        return f"A {self.name} cell with Klf4 {'present' if self.Klf4_present else 'absent'}, currently {self.differentiation_status}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("environment")
        myeloid_cell_with_Klf4 = MyeloidCell("myeloid_cell_with_Klf4", Klf4_present=True)
        myeloid_cell_without_Klf4 = MyeloidCell("myeloid_cell_without_Klf4", Klf4_present=False)
        world.addObject(myeloid_cell_with_Klf4)
        world.addObject(myeloid_cell_without_Klf4)
        return world

    def run_simulation(self):
        for cell in self.rootObject.contains:
            cell.differentiate()

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
