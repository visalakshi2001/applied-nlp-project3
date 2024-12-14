
# Claim: Sympathetic nerve activity is elevated throughout normal pregnancy.
# The simulation will test the sympathetic nerve activity in pregnant and nonpregnant women.

from simulation_utils import GameObject, Container

class SympatheticNerveActivity(GameObject):
    def __init__(self, name, sympathetic_activity=0):
        super().__init__(name)
        self.properties = {
            "sympathetic_activity": sympathetic_activity
        }

    def tick(self):
        # Simulate sympathetic activity changes
        if self.name == "pregnant_woman":
            self.properties["sympathetic_activity"] += 1  # Increase activity for pregnant women
        elif self.name == "nonpregnant_woman":
            self.properties["sympathetic_activity"] += 0.5  # Increase activity for nonpregnant women

    def makeDescriptionStr(self):
        return f"{self.name} has a sympathetic nerve activity level of {self.properties['sympathetic_activity']}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

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
        pregnant_woman = SympatheticNerveActivity("pregnant_woman")
        nonpregnant_woman = SympatheticNerveActivity("nonpregnant_woman")
        world.addObject(pregnant_woman)
        world.addObject(nonpregnant_woman)        
        return world

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
            # Perform a tick to simulate time passing
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate for a few ticks to observe changes in sympathetic activity
    for _ in range(5):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Determine if the claim is supported or refuted
    pregnant_activity = simulation.rootObject.contains[0].properties["sympathetic_activity"]
    nonpregnant_activity = simulation.rootObject.contains[1].properties["sympathetic_activity"]

    if pregnant_activity > nonpregnant_activity:
        print("Claim Supported: Sympathetic nerve activity is elevated throughout normal pregnancy.")
    else:
        print("Claim Refuted: Sympathetic nerve activity is not elevated throughout normal pregnancy.")

if __name__ == "__main__":
    main()
