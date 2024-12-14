
# Claim: The myocardial cell lineage originally develops from cardiac progenitors of exclusively endodermal origin.
# The simulation will test the claim against the reference text which indicates that the myocardial cell lineage develops from mesoderm-derived lineages.

from simulation_utils import GameObject, Container

class CardiacProgenitor(GameObject):
    def __init__(self, name, origin):
        super().__init__(name)
        self.properties = {
            "origin": origin,  # Origin can be 'endoderm' or 'mesoderm'
            "lineages": []     # Lineages derived from this progenitor
        }

    def differentiate(self):
        if self.properties["origin"] == "mesoderm":
            self.properties["lineages"] = ["cardiomyocytes", "endothelial cells", "vascular smooth muscle cells"]
        else:
            self.properties["lineages"] = ["unknown lineage"]

    def makeDescriptionStr(self):
        description = f"A {self.name} of {self.properties['origin']} origin, which can differentiate into: {', '.join(self.properties['lineages'])}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("Cardiac Development Environment")
        mesoderm_progenitor = CardiacProgenitor("Mesodermal Progenitor", "mesoderm")
        endoderm_progenitor = CardiacProgenitor("Endodermal Progenitor", "endoderm")
        
        mesoderm_progenitor.differentiate()
        endoderm_progenitor.differentiate()
        
        world.addObject(mesoderm_progenitor)
        world.addObject(endoderm_progenitor)
        
        return world

    def run(self):
        return self.observationStr

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
