
# Claim: Chenodeoxycholic acid treatment decreases brown adipose tissue activity.
# The simulation will test the effect of chenodeoxycholic acid (CDCA) on brown adipose tissue (BAT) activity.

from simulation_utils import GameObject, Container

class BrownAdiposeTissue(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.activity_level = activity_level

    def increase_activity(self):
        self.activity_level += 1

    def decrease_activity(self):
        self.activity_level -= 1

    def makeDescriptionStr(self):
        return f"{self.name} with activity level: {self.activity_level}"

class ChenodeoxycholicAcid(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def treat(self, bat):
        # According to the claim, CDCA treatment should decrease BAT activity
        bat.decrease_activity()

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        bat = BrownAdiposeTissue("Brown Adipose Tissue", activity_level=5)  # Initial activity level
        cdca = ChenodeoxycholicAcid("Chenodeoxycholic Acid")
        world.addObject(bat)
        world.addObject(cdca)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("treat with Chenodeoxycholic Acid", ["treat", allObjects["Chenodeoxycholic Acid"][0], allObjects["Brown Adipose Tissue"][0]])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "treat":
            cdca = action[1]
            bat = action[2]
            cdca.treat(bat)
            self.observationStr = f"{cdca.name} has been applied to {bat.name}."
        
        self.doWorldTick()
        self.generatePossibleActions()
        return self.observationStr

    def doWorldTick(self):
        pass

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "treat with Chenodeoxycholic Acid"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final observation to check the activity level of BAT
    bat = simulation.rootObject.containsItemWithName("Brown Adipose Tissue")[0]
    print(f"Final activity level of BAT: {bat.activity_level}")
    if bat.activity_level < 5:
        print("Claim Supported: Chenodeoxycholic acid treatment decreases brown adipose tissue activity.")
    else:
        print("Claim Refuted: Chenodeoxycholic acid treatment does not decrease brown adipose tissue activity.")

if __name__ == "__main__":
    main()
