
# Claim: Treatment with a protein named FN restores regenerative abilities of aged muscles.
# The simulation will model the effects of fibronectin (FN) on muscle stem cells (MuSCs) in aged muscles.

from simulation_utils import GameObject, Container

class MuscleStemCell(GameObject):
    def __init__(self, name, fn_level=0):
        super().__init__(name)
        self.fn_level = fn_level  # Level of fibronectin available
        self.regeneration_ability = 0  # Regeneration ability of the stem cell

    def tick(self):
        # If FN level is sufficient, restore regeneration ability
        if self.fn_level > 0:
            self.regeneration_ability = 1  # Restores youth-like regeneration
        else:
            self.regeneration_ability = 0  # No regeneration ability

    def makeDescriptionStr(self):
        return f"{self.name} with FN level: {self.fn_level}, regeneration ability: {self.regeneration_ability}"

class AgedMuscle(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.stem_cells = []

    def addStemCell(self, stem_cell):
        self.stem_cells.append(stem_cell)

    def tick(self):
        for stem_cell in self.stem_cells:
            stem_cell.tick()

    def makeDescriptionStr(self):
        description = f"{self.name} contains:\n"
        for stem_cell in self.stem_cells:
            description += "\t" + stem_cell.makeDescriptionStr() + "\n"
        return description

class FNInjection(GameObject):
    def __init__(self, name, fn_amount):
        super().__init__(name)
        self.fn_amount = fn_amount

    def apply(self, aged_muscle):
        for stem_cell in aged_muscle.stem_cells:
            stem_cell.fn_level += self.fn_amount  # Increase FN level in stem cells

class World(Container):
    def __init__(self):
        super().__init__("muscle regeneration environment")

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
        aged_muscle = AgedMuscle("Aged Muscle")
        stem_cell1 = MuscleStemCell("MuSC 1")
        stem_cell2 = MuscleStemCell("MuSC 2")
        aged_muscle.addStemCell(stem_cell1)
        aged_muscle.addStemCell(stem_cell2)
        world.addObject(aged_muscle)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("inject FN", ["inject", 5])  # Inject 5 units of FN

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
        elif actionVerb == "inject":
            fn_injection = FNInjection("FN Injection", action[1])
            fn_injection.apply(self.rootObject.contains[0])  # Apply to the aged muscle
            self.observationStr = f"Injected {action[1]} units of FN into the aged muscle."

        # Update the state of the world
        self.rootObject.contains[0].tick()  # Tick the aged muscle to update stem cells

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "inject FN"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the regeneration ability after FN injection
    stem_cells = simulation.rootObject.contains[0].stem_cells
    regeneration_status = all(stem_cell.regeneration_ability == 1 for stem_cell in stem_cells)
    if regeneration_status:
        print("Claim Supported: FN restores regenerative abilities of aged muscles.")
    else:
        print("Claim Refuted: FN does not restore regenerative abilities of aged muscles.")

if __name__ == "__main__":
    main()
