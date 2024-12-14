
# Claim: KRT17 modulates the expression of the transcriptional regulator AIRE in diseased epithelia.
# The simulation will model the interaction between KRT17 and AIRE in keratinocytes.

from simulation_utils import GameObject, Container

class Keratinocyte(GameObject):
    def __init__(self, name, KRT17_expression=0, AIRE_expression=0):
        super().__init__(name)
        self.properties = {
            "KRT17_expression": KRT17_expression,
            "AIRE_expression": AIRE_expression
        }

    def tick(self):
        # AIRE expression is dependent on KRT17 expression
        self.properties["AIRE_expression"] = self.properties["KRT17_expression"] * 2  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        description = f"A {self.name} with KRT17 expression level {self.properties['KRT17_expression']} and AIRE expression level {self.properties['AIRE_expression']}."
        return description

class TumorKeratinocyte(Keratinocyte):
    def __init__(self, name):
        super().__init__(name, KRT17_expression=5)  # Set a high KRT17 expression for tumor keratinocytes

class World(Container):
    def __init__(self):
        super().__init__("diseased epithelia")
        self.addObject(TumorKeratinocyte("tumor_keratinocyte_1"))

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.doWorldTick()

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Check the expression levels to verify the claim
    tumor_keratinocyte = simulation.rootObject.contains[0]
    KRT17_expression = tumor_keratinocyte.properties["KRT17_expression"]
    AIRE_expression = tumor_keratinocyte.properties["AIRE_expression"]

    if AIRE_expression > 0 and KRT17_expression > 0:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"KRT17 expression: {KRT17_expression}, AIRE expression: {AIRE_expression}")
    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
