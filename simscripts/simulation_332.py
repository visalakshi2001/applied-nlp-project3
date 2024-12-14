
# Claim: Depletion of T-helper 17 (Th17) cells during simian immunodeficiency virus (SIV) infection decreases dissemination of Salmonella Typhimurium from the gut.

# Importing necessary classes from the base template
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
            self.properties["can_prevent_dissemination"] = False
        else:
            self.properties["can_prevent_dissemination"] = True

class SalmonellaTyphimurium(GameObject):
    def __init__(self, name, can_disseminate=False):
        super().__init__(name)
        self.properties = {
            "can_disseminate": can_disseminate
        }

    def tick(self):
        # If Th17 cells are depleted, Salmonella can disseminate
        if not self.parent.getProperty("can_prevent_dissemination"):
            self.properties["can_disseminate"] = True
        else:
            self.properties["can_disseminate"] = False

class SIVInfection(Container):
    def __init__(self):
        super().__init__("SIV Infection")
        self.th17_cells = Th17Cell("Th17 Cells", is_depleted=True)
        self.salmonella = SalmonellaTyphimurium("Salmonella Typhimurium", can_disseminate=False)
        self.addObject(self.th17_cells)
        self.addObject(self.salmonella)

    def tick(self):
        self.th17_cells.tick()
        self.salmonella.tick()

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.siv_infection = SIVInfection()
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
        self.rootObject.tick()

        # Check the state of Salmonella dissemination
        if self.rootObject.siv_infection.salmonella.properties["can_disseminate"]:
            self.observationStr += "Salmonella Typhimurium is disseminating due to Th17 cell depletion.\n"
        else:
            self.observationStr += "Salmonella Typhimurium is not disseminating due to Th17 cell presence.\n"

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
