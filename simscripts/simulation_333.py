
# Claim: Depletion of T-helper 17 (Th17) cells during simian immunodeficiency virus (SIV) infection increases dissemination of Salmonella Typhimurium from the gut.

from simulation_utils import GameObject, Container

class Th17Cell(GameObject):
    def __init__(self, name, is_depleted=False):
        super().__init__(name)
        self.properties = {
            "is_depleted": is_depleted
        }

    def tick(self):
        # If Th17 cells are depleted, they cannot perform their function
        if self.properties["is_depleted"]:
            self.properties["dissemination_inhibition"] = False
        else:
            self.properties["dissemination_inhibition"] = True

class SalmonellaTyphimurium(GameObject):
    def __init__(self, name, can_disseminate=False):
        super().__init__(name)
        self.properties = {
            "can_disseminate": can_disseminate
        }

    def tick(self):
        # If Th17 cells are depleted, Salmonella can disseminate
        if not self.properties["can_disseminate"]:
            self.properties["can_disseminate"] = True

class SIVInfection(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.th17_cells = Th17Cell("Th17 Cells", is_depleted=True)
        self.salmonella = SalmonellaTyphimurium("Salmonella Typhimurium", can_disseminate=False)

    def tick(self):
        # Simulate the effect of SIV infection on Th17 cells and Salmonella dissemination
        self.th17_cells.tick()
        self.salmonella.tick()

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.siv_infection = SIVInfection("SIV Infection")
        self.addObject(self.siv_infection)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += f"\t{self.siv_infection.makeDescriptionStr()}\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Do one tick of the environment
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    simulation.step("look")
    
    # Check the state of Th17 cells and Salmonella dissemination
    th17_depleted = simulation.rootObject.siv_infection.th17_cells.properties["is_depleted"]
    salmonella_can_disseminate = simulation.rootObject.siv_infection.salmonella.properties["can_disseminate"]

    if th17_depleted and salmonella_can_disseminate:
        print("Claim Supported: Depletion of Th17 cells increases dissemination of Salmonella Typhimurium.")
    else:
        print("Claim Refuted: Depletion of Th17 cells does not increase dissemination of Salmonella Typhimurium.")

if __name__ == "__main__":
    main()
