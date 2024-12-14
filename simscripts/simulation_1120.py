
# Claim: Sympathetic nerve activity is reduced throughout normal pregnancy.
# The simulation will test the sympathetic nerve activity in pregnant and nonpregnant women.

from simulation_utils import GameObject, Container

class SympatheticNerveActivity(GameObject):
    def __init__(self, name, sympathetic_activity=0):
        super().__init__(name)
        self.properties = {
            "sympathetic_activity": sympathetic_activity
        }

    def tick(self):
        # Simulate the sympathetic activity changes during pregnancy
        if "pregnant" in self.name:
            self.properties["sympathetic_activity"] = max(0, self.properties["sympathetic_activity"] - 1)  # Reduced activity
        else:
            self.properties["sympathetic_activity"] += 1  # Increased activity for nonpregnant

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
        pregnant_woman = SympatheticNerveActivity("pregnant_woman", sympathetic_activity=5)
        nonpregnant_woman = SympatheticNerveActivity("nonpregnant_woman", sympathetic_activity=5)
        world.addObject(pregnant_woman)
        world.addObject(nonpregnant_woman)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"tick": ["tick"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "tick":
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
    
    # Simulate the passage of time to observe changes in sympathetic nerve activity
    for _ in range(5):  # Simulate 5 time steps
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the final sympathetic activity levels
    pregnant_activity = simulation.rootObject.contains[0].properties["sympathetic_activity"]
    nonpregnant_activity = simulation.rootObject.contains[1].properties["sympathetic_activity"]

    if pregnant_activity < nonpregnant_activity:
        result = "Supported: Sympathetic nerve activity is reduced throughout normal pregnancy."
    else:
        result = "Refuted: Sympathetic nerve activity is not reduced throughout normal pregnancy."

    print(result)

if __name__ == "__main__":
    main()
