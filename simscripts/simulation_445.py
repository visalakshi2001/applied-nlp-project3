
# Claim: GATA3 regulates self-renewal capacity in bone marrow hematopoietic stem cells.
# The simulation will model the effect of GATA3 on hematopoietic stem cells (HSCs) and their self-renewal capacity.

from simulation_utils import GameObject, Container

class HematopoieticStemCell(GameObject):
    def __init__(self, name, is_quiescent=True, has_GATA3=True):
        super().__init__(name)
        self.properties = {
            "is_quiescent": is_quiescent,  # Indicates if the cell is in a quiescent state
            "has_GATA3": has_GATA3,        # Indicates if the cell has GATA3
            "in_cycle": False               # Indicates if the cell is in the cell cycle
        }

    def tick(self):
        # If the cell has GATA3, it can enter the cell cycle
        if self.properties["has_GATA3"] and self.properties["is_quiescent"]:
            self.properties["in_cycle"] = True
            self.properties["is_quiescent"] = False  # It is no longer quiescent
        elif not self.properties["has_GATA3"]:
            self.properties["in_cycle"] = False  # Without GATA3, it cannot enter the cycle

    def makeDescriptionStr(self):
        return f"{self.name}: Quiescent: {self.properties['is_quiescent']}, In Cycle: {self.properties['in_cycle']}, Has GATA3: {self.properties['has_GATA3']}"

class Gata3NullHSC(HematopoieticStemCell):
    def __init__(self, name):
        super().__init__(name, has_GATA3=False)

class World(Container):
    def __init__(self):
        super().__init__("Bone Marrow Environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        # Create normal HSCs with GATA3
        hsc1 = HematopoieticStemCell("HSC with GATA3")
        hsc2 = HematopoieticStemCell("HSC with GATA3")
        # Create GATA3-null HSCs
        gata3_null_hsc1 = Gata3NullHSC("GATA3-null HSC")
        gata3_null_hsc2 = Gata3NullHSC("GATA3-null HSC")
        
        world.addObject(hsc1)
        world.addObject(hsc2)
        world.addObject(gata3_null_hsc1)
        world.addObject(gata3_null_hsc2)
        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"tick": ["tick"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            # Perform a tick for all cells
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the passage of time to observe the effects of GATA3
    for _ in range(3):  # Simulate 3 ticks
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
