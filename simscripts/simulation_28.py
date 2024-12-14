
# Claim: A T helper 2 cell (Th2) environment impedes disease development in patients with systemic lupus erythematosus (SLE).
# The simulation will model the relationship between T helper 2 cells, basophils, and disease activity in SLE.

from simulation_utils import GameObject, Container

class THelperCell(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.properties = {
            "activity_level": activity_level  # Represents the activity level of Th2 cells
        }

    def tick(self):
        # Simulate the effect of Th2 cell activity on disease development
        if self.properties["activity_level"] > 5:
            self.properties["activity_level"] = 5  # Cap the activity level
        # Higher activity level of Th2 cells is assumed to reduce disease activity
        self.properties["disease_activity"] = max(0, 10 - self.properties["activity_level"])

    def makeDescriptionStr(self):
        return f"A {self.name} with an activity level of {self.properties['activity_level']} and disease activity level of {self.properties.get('disease_activity', 10)}."

class Basophil(GameObject):
    def __init__(self, name, activation_level=0):
        super().__init__(name)
        self.properties = {
            "activation_level": activation_level  # Represents the activation level of basophils
        }

    def tick(self):
        # Simulate the effect of basophil activation on Th2 cells
        if self.properties["activation_level"] > 5:
            self.properties["activation_level"] = 5  # Cap the activation level
        # Higher activation level of basophils is assumed to increase Th2 cell activity
        self.properties["th2_activity_influence"] = self.properties["activation_level"]

    def makeDescriptionStr(self):
        return f"A {self.name} with an activation level of {self.properties['activation_level']}."

class World(Container):
    def __init__(self):
        super().__init__("SLE Environment")

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
        th2_cell = THelperCell("Th2 Cell", activity_level=3)  # Initial activity level
        basophil = Basophil("Basophil", activation_level=4)  # Initial activation level
        world.addObject(th2_cell)
        world.addObject(basophil)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("increase Th2 activity", ["increase", "Th2 Cell"])
        self.addAction("increase basophil activation", ["increase", "Basophil"])

    def actionIncrease(self, obj_name):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if obj.name == obj_name:
                if isinstance(obj, THelperCell):
                    obj.properties["activity_level"] += 1
                elif isinstance(obj, Basophil):
                    obj.properties["activation_level"] += 1
                return f"You increase the {obj_name}."
        return f"{obj_name} not found."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            self.observationStr = self.actionIncrease(action[1])

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
    actions = ["increase Th2 activity", "increase basophil activation", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
