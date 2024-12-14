
# Claim: CD44v6 is not associated with constitutive and reprogrammed cancer stem cells driving cancer metastasis.
# The simulation will test the association of CD44v6 with cancer stem cells and their role in metastasis.

from simulation_utils import GameObject, Container

class CancerStemCell(GameObject):
    def __init__(self, name, cd44v6_expression=False, metastatic_capacity=False):
        super().__init__(name)
        self.properties = {
            "cd44v6_expression": cd44v6_expression,
            "metastatic_capacity": metastatic_capacity
        }

    def express_cd44v6(self):
        self.properties["cd44v6_expression"] = True
        self.properties["metastatic_capacity"] = True  # If CD44v6 is expressed, it gains metastatic capacity

    def makeDescriptionStr(self):
        return f"{self.name} - CD44v6 Expression: {self.properties['cd44v6_expression']}, Metastatic Capacity: {self.properties['metastatic_capacity']}"

class Cytokine(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def activate_cd44v6_expression(self, cancer_stem_cell):
        cancer_stem_cell.express_cd44v6()

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("Cancer Environment")
        cr_csc = CancerStemCell("Colorectal Cancer Stem Cell (CR-CSC)")
        cytokine_hgf = Cytokine("Hepatocyte Growth Factor (HGF)")
        cytokine_opn = Cytokine("Osteopontin (OPN)")
        cytokine_sdf1 = Cytokine("Stromal-Derived Factor 1α (SDF-1)")

        world.addObject(cr_csc)
        world.addObject(cytokine_hgf)
        world.addObject(cytokine_opn)
        world.addObject(cytokine_sdf1)

        # Simulate the effect of cytokines on the cancer stem cell
        cytokine_hgf.activate_cd44v6_expression(cr_csc)
        cytokine_opn.activate_cd44v6_expression(cr_csc)
        cytokine_sdf1.activate_cd44v6_expression(cr_csc)

        return world

    def run_simulation(self):
        return self.observationStr

def main():
    simulation = Simulation()
    result = simulation.run_simulation()
    print(result)

    # Check the properties of the cancer stem cell to determine the claim's validity
    cr_csc = simulation.rootObject.containsItemWithName("Colorectal Cancer Stem Cell (CR-CSC)")[0]
    if cr_csc.properties["cd44v6_expression"] and cr_csc.properties["metastatic_capacity"]:
        print("Claim Refuted: CD44v6 is associated with cancer stem cells driving metastasis.")
    else:
        print("Claim Supported: CD44v6 is not associated with cancer stem cells driving metastasis.")

if __name__ == "__main__":
    main()
