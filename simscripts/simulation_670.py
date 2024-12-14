
# Claim: Knockout proximal tubule-specific deletion of the BMP receptor Alk3 causes epithelial damage.
# The simulation will model the effects of Alk3 deletion on epithelial damage in the kidney.

from simulation_utils import GameObject, Container

class KidneyCell(GameObject):
    def __init__(self, name, alk3_present=True):
        super().__init__(name)
        self.properties = {
            "alk3_present": alk3_present,
            "epithelial_damage": 0  # 0 means no damage, higher values indicate more damage
        }

    def tick(self):
        if not self.properties["alk3_present"]:
            # If Alk3 is not present, increase epithelial damage
            self.properties["epithelial_damage"] += 1  # Increment damage for each tick without Alk3

    def makeDescriptionStr(self):
        return f"A {self.name} cell with Alk3 present: {self.properties['alk3_present']}, epithelial damage level: {self.properties['epithelial_damage']}."

class Kidney(Container):
    def __init__(self):
        super().__init__("kidney")
        self.addObject(KidneyCell("proximal_tubule_cell_1", alk3_present=True))
        self.addObject(KidneyCell("proximal_tubule_cell_2", alk3_present=False))  # Simulating Alk3 knockout

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        kidney = Kidney()
        return kidney

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            self.doWorldTick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate several ticks to observe the epithelial damage
    for _ in range(5):
        print("Ticking the simulation...")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the epithelial damage level
    damage_level = simulation.rootObject.contains[1].properties["epithelial_damage"]  # Check the second cell (knockout)
    if damage_level > 0:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
