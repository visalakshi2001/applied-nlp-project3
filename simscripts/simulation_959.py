
# Claim: Polymeal nutrition increases cardiovascular mortality.
# The simulation will model the effects of the Polymeal on cardiovascular health.

from simulation_utils import GameObject, Container

class Polymeal(GameObject):
    def __init__(self, name, daily_intake=0):
        super().__init__(name)
        self.properties = {
            "daily_intake": daily_intake,
            "cardiovascular_events_reduction": 76,  # percentage reduction in cardiovascular events
            "life_expectancy_increase": 6.6,  # years for men
            "life_expectancy_free_disease": 9.0,  # years for men
            "life_expectancy_with_disease": -2.4  # years for men
        }

    def tick(self):
        # Simulate the effect of daily intake of Polymeal
        if self.properties["daily_intake"] > 0:
            # Assuming that daily intake leads to a reduction in cardiovascular events
            self.properties["cardiovascular_events_reduction"] = 76
            self.properties["life_expectancy_increase"] = 6.6
            self.properties["life_expectancy_free_disease"] = 9.0
            self.properties["life_expectancy_with_disease"] = -2.4
        else:
            # No intake leads to no benefits
            self.properties["cardiovascular_events_reduction"] = 0
            self.properties["life_expectancy_increase"] = 0
            self.properties["life_expectancy_free_disease"] = 0
            self.properties["life_expectancy_with_disease"] = 0

    def makeDescriptionStr(self):
        description = (f"A {self.name} with daily intake of {self.properties['daily_intake']} servings, "
                       f"which reduces cardiovascular events by {self.properties['cardiovascular_events_reduction']}%, "
                       f"increases life expectancy by {self.properties['life_expectancy_increase']} years, "
                       f"and decreases life expectancy with cardiovascular disease by {self.properties['life_expectancy_with_disease']} years.")
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
        polymeal = Polymeal("Polymeal")
        world.addObject(polymeal)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        for obj in allObjects:
            if isinstance(obj, Polymeal):
                self.addAction("increase daily intake of " + obj.name, ["increase", obj])
                self.addAction("decrease daily intake of " + obj.name, ["decrease", obj])

    def actionIncrease(self, polymeal):
        polymeal.properties["daily_intake"] += 1
        return f"You increase the daily intake of {polymeal.name} by 1 serving."

    def actionDecrease(self, polymeal):
        if polymeal.properties["daily_intake"] > 0:
            polymeal.properties["daily_intake"] -= 1
            return f"You decrease the daily intake of {polymeal.name} by 1 serving."
        else:
            return f"{polymeal.name} daily intake cannot be decreased below 0."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb.startswith("increase"):
            self.observationStr = self.actionIncrease(action[1])
        elif actionVerb.startswith("decrease"):
            self.observationStr = self.actionDecrease(action[1])

        self.doWorldTick()
        self.generatePossibleActions()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase daily intake of Polymeal", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the final properties to determine if the claim is supported or refuted
    polymeal = simulation.rootObject.containsItemWithName("Polymeal")[0]
    if polymeal.properties["cardiovascular_events_reduction"] > 0:
        print("Claim Supported: Polymeal nutrition reduces cardiovascular mortality.")
    else:
        print("Claim Refuted: Polymeal nutrition does not reduce cardiovascular mortality.")

if __name__ == "__main__":
    main()
