
# Claim: Mice lacking Sirt1 in Sf1-expressing neurons have increased susceptibility to diet-induced obesity and insulin resistance.
# The simulation will model the effects of SIRT1 on mice in relation to diet-induced obesity and insulin resistance.

from simulation_utils import GameObject, Container

class Mouse(GameObject):
    def __init__(self, name, sirt1_present=True):
        super().__init__(name)
        self.sirt1_present = sirt1_present
        self.properties = {
            "susceptibility_to_obesity": 0,
            "insulin_resistance": 0
        }

    def tick(self):
        if not self.sirt1_present:
            self.properties["susceptibility_to_obesity"] += 1  # Increased susceptibility
            self.properties["insulin_resistance"] += 1  # Increased insulin resistance

    def makeDescriptionStr(self):
        description = f"A {self.name} with SIRT1 {'present' if self.sirt1_present else 'absent'}, susceptibility to obesity: {self.properties['susceptibility_to_obesity']}, insulin resistance: {self.properties['insulin_resistance']}."
        return description

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
        mouse_with_sirt1 = Mouse("Mouse with SIRT1", sirt1_present=True)
        mouse_without_sirt1 = Mouse("Mouse without SIRT1", sirt1_present=False)
        world.addObject(mouse_with_sirt1)
        world.addObject(mouse_without_sirt1)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            # Perform a tick to simulate the passage of time
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the effects over a few ticks
    for _ in range(5):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
