
# Claim: Intake of folic acid (FA) and vitamin B6 (VB6) reduces levels of homocysteine.
# The simulation will model the relationship between folic acid, vitamin B6 intake, and homocysteine levels.

from simulation_utils import GameObject, Container

class Vitamin(GameObject):
    def __init__(self, name, intake=0):
        super().__init__(name)
        self.intake = intake
        self.properties = {
            "intake": intake,
            "homocysteine_level": 10  # Starting homocysteine level
        }

    def tick(self):
        # Simulate the effect of vitamin intake on homocysteine levels
        if self.intake > 0:
            self.properties["homocysteine_level"] -= self.intake * 0.5  # Arbitrary reduction factor
        # Ensure homocysteine level does not go below 0
        self.properties["homocysteine_level"] = max(self.properties["homocysteine_level"], 0)

    def makeDescriptionStr(self):
        return f"{self.name} intake: {self.intake}, Homocysteine level: {self.properties['homocysteine_level']}"

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
        folic_acid = Vitamin("Folic Acid", intake=5)  # Simulating intake of 5 units
        vitamin_b6 = Vitamin("Vitamin B6", intake=3)  # Simulating intake of 3 units
        world.addObject(folic_acid)
        world.addObject(vitamin_b6)
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
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the final homocysteine levels to determine if the claim is supported or refuted
    folic_acid = simulation.rootObject.containsItemWithName("Folic Acid")[0]
    vitamin_b6 = simulation.rootObject.containsItemWithName("Vitamin B6")[0]
    final_homocysteine_level = folic_acid.properties["homocysteine_level"]
    
    if final_homocysteine_level < 10:  # Initial level was 10
        print("Claim Supported: Intake of folic acid and vitamin B6 reduces levels of homocysteine.")
    else:
        print("Claim Refuted: Intake of folic acid and vitamin B6 does not reduce levels of homocysteine.")

if __name__ == "__main__":
    main()
