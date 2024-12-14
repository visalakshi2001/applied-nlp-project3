
# Claim: Nonhuman primates are incapable of producing neutralizing antibodies in response to the Eilat virus (EILV) produced in mosquitos.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class NonhumanPrimate(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "neutralizing_antibodies": False,
            "immune_response": False
        }

    def elicit_response(self):
        # Simulate the immune response to EILV/CHIKV
        self.properties["neutralizing_antibodies"] = True
        self.properties["immune_response"] = True

    def makeDescriptionStr(self):
        description = f"A {self.name} with neutralizing antibodies: {self.properties['neutralizing_antibodies']} and immune response: {self.properties['immune_response']}."
        return description

class EILV(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "elicits_immunity": True
        }

    def makeDescriptionStr(self):
        return f"{self.name} that elicits immunity: {self.properties['elicits_immunity']}."

# The world is the root object of the game object tree.
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
        primate = NonhumanPrimate("nonhuman_primate")
        eilv = EILV("Eilat virus (EILV)")
        world.addObject(primate)
        world.addObject(eilv)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("elicit immune response", ["elicit", allObjects["nonhuman_primate"][0]])

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def actionElicit(self, primate):
        if isinstance(primate, NonhumanPrimate):
            primate.elicit_response()
            return f"The {primate.name} has elicited an immune response."
        return "Invalid action."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "elicit":
            self.observationStr = self.actionElicit(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "elicit immune response"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the result of the simulation to determine if the claim is supported or refuted
    primate = simulation.rootObject.containsItemWithName("nonhuman_primate")[0]
    if primate.properties["neutralizing_antibodies"]:
        print("Claim is Refuted: Nonhuman primates can produce neutralizing antibodies in response to EILV.")
    else:
        print("Claim is Supported: Nonhuman primates are incapable of producing neutralizing antibodies in response to EILV.")

if __name__ == "__main__":
    main()
