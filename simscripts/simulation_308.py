
# Claim: DUSP4 downregulation deactivates the Ras-ERK pathway

from simulation_utils import GameObject, Container

class DUSP4(GameObject):
    def __init__(self, name, concentration=0):
        super().__init__(name)
        self.concentration = concentration  # Represents the concentration of DUSP4

    def tick(self):
        # Simulate the effect of DUSP4 concentration on the Ras-ERK pathway
        if self.concentration < 1:  # Assuming low concentration activates the pathway
            return "Ras-ERK pathway is activated."
        else:
            return "Ras-ERK pathway is deactivated."

class RasERKPathway(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def status(self):
        return "active" if self.active else "inactive"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        dusp4 = DUSP4("DUSP4", concentration=0)  # Low concentration to simulate downregulation
        ras_erk_pathway = RasERKPathway("Ras-ERK Pathway")
        
        # Simulate the effect of DUSP4 on the Ras-ERK pathway
        if dusp4.concentration < 1:
            ras_erk_pathway.activate()
        else:
            ras_erk_pathway.deactivate()

        world.addObject(dusp4)
        world.addObject(ras_erk_pathway)
        return world

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += f"\t{obj.name} with concentration {obj.concentration if isinstance(obj, DUSP4) else ''}.\n"
            if isinstance(obj, RasERKPathway):
                outStr += f"\tRas-ERK Pathway is currently {obj.status()}.\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
