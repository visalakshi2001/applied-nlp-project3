
# Claim: Oat tolerant coeliac patients may have oat specific inflammatory cells in their small bowel mucosa.
# This simulation will check if oat-specific inflammatory cells exist in oat-tolerant coeliac patients.

from simulation_utils import GameObject, Container

class TCell(GameObject):
    def __init__(self, name, specific_to_oats=False):
        super().__init__(name)
        self.specific_to_oats = specific_to_oats

    def makeDescriptionStr(self):
        specificity = "specific to oats" if self.specific_to_oats else "not specific to oats"
        return f"A T-cell named {self.name}, which is {specificity}."

class Patient(GameObject):
    def __init__(self, name, has_inflammation=False):
        super().__init__(name)
        self.has_inflammation = has_inflammation
        self.t_cells = []

    def addTCell(self, t_cell):
        self.t_cells.append(t_cell)

    def checkOatSpecificCells(self):
        return any(t_cell.specific_to_oats for t_cell in self.t_cells)

    def makeDescriptionStr(self):
        inflammation_status = "has inflammation" if self.has_inflammation else "does not have inflammation"
        return f"Patient {self.name}, who {inflammation_status}, has {len(self.t_cells)} T-cells."

class World(Container):
    def __init__(self):
        super().__init__("environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        patient1 = Patient("Patient 1", has_inflammation=True)
        patient2 = Patient("Patient 2", has_inflammation=False)

        # Adding T-cells to patients
        t_cell1 = TCell("T-cell 1", specific_to_oats=True)
        t_cell2 = TCell("T-cell 2", specific_to_oats=False)
        t_cell3 = TCell("T-cell 3", specific_to_oats=True)

        patient1.addTCell(t_cell1)
        patient1.addTCell(t_cell2)
        patient2.addTCell(t_cell3)

        world.addObject(patient1)
        world.addObject(patient2)
        
        return world

    def checkClaim(self):
        # Check if any patient has oat-specific T-cells
        for patient in self.rootObject.contains:
            if patient.checkOatSpecificCells():
                return "Claim Supported: Oat specific inflammatory cells found in oat tolerant coeliac patients."
        return "Claim Refuted: No oat specific inflammatory cells found."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.checkClaim()
    print(result)

if __name__ == "__main__":
    main()
