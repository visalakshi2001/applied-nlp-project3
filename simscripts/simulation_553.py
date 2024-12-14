
# Claim: IgA plasma cells that are specific for transglutaminase 2 are scarce in the duodenal mucosa of celiac disease patients when the disease is active.

from simulation_utils import GameObject, Container

class PlasmaCell(GameObject):
    def __init__(self, name, is_specific=False):
        super().__init__(name)
        self.properties = {
            "is_specific": is_specific
        }

class DuodenalMucosa(Container):
    def __init__(self):
        super().__init__("duodenal mucosa")
        self.properties["is_active"] = True  # Indicates if the celiac disease is active

class CeliacDiseaseSimulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.check_plasma_cells()

    def _initialize_simulation(self):
        world = DuodenalMucosa()
        # Adding TG2 specific plasma cells
        for i in range(5):  # Adding 5 specific plasma cells
            plasma_cell = PlasmaCell(f"TG2_specific_plasma_cell_{i+1}", is_specific=True)
            world.addObject(plasma_cell)
        # Adding non-specific plasma cells
        for i in range(10):  # Adding 10 non-specific plasma cells
            plasma_cell = PlasmaCell(f"non_specific_plasma_cell_{i+1}", is_specific=False)
            world.addObject(plasma_cell)
        return world

    def check_plasma_cells(self):
        specific_cells = self.rootObject.containsItemWithName("TG2_specific_plasma_cell")
        if len(specific_cells) > 0:
            self.result = "Supported"
        else:
            self.result = "Refuted"

    def makeDescriptionStr(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = CeliacDiseaseSimulation()
    print(simulation.observationStr)
    print(f"Claim verification result: {simulation.result}")

if __name__ == "__main__":
    main()
