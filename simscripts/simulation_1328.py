
# Claim: Tuberculosis-induced granulomas express different immune system protein signatures than the surrounding tissue.
# The simulation will model granulomas and surrounding tissue to compare their immune protein signatures.

from simulation_utils import GameObject, Container

class ImmuneCell(GameObject):
    def __init__(self, name, signature):
        super().__init__(name)
        self.properties = {
            "signature": signature  # immune protein signature
        }

    def makeDescriptionStr(self):
        return f"{self.name} with signature: {self.properties['signature']}."

class Granuloma(Container):
    def __init__(self):
        super().__init__("Granuloma")
        # Pro-inflammatory environment
        self.addObject(ImmuneCell("Pro-inflammatory Cell 1", "antimicrobial peptides"))
        self.addObject(ImmuneCell("Pro-inflammatory Cell 2", "reactive oxygen species"))
        self.addObject(ImmuneCell("Pro-inflammatory Cell 3", "pro-inflammatory eicosanoids"))

class SurroundingTissue(Container):
    def __init__(self):
        super().__init__("Surrounding Tissue")
        # Anti-inflammatory environment
        self.addObject(ImmuneCell("Anti-inflammatory Cell 1", "anti-inflammatory cytokines"))
        self.addObject(ImmuneCell("Anti-inflammatory Cell 2", "inhibitory receptors"))

class World(Container):
    def __init__(self):
        super().__init__("TB Environment")
        self.addObject(Granuloma())
        self.addObject(SurroundingTissue())

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def compareSignatures(self):
        granuloma = self.rootObject.contains[0]  # Granuloma
        surrounding_tissue = self.rootObject.contains[1]  # Surrounding Tissue

        granuloma_signatures = [cell.properties['signature'] for cell in granuloma.contains]
        surrounding_signatures = [cell.properties['signature'] for cell in surrounding_tissue.contains]

        # Check if the signatures are different
        if set(granuloma_signatures) != set(surrounding_signatures):
            return "Claim Supported: Granulomas express different immune system protein signatures than the surrounding tissue."
        else:
            return "Claim Refuted: Granulomas do not express different immune system protein signatures than the surrounding tissue."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.compareSignatures()
    print(result)

if __name__ == "__main__":
    main()
