
# Claim: The peak incidence of fractures occurs in toddlers.
# The simulation will check the age range for peak incidence of fractures based on the provided reference text.

from simulation_utils import GameObject, Container

class Child(GameObject):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age  # Age of the child
        self.properties = {
            "fracture_incidence": 0  # Initial incidence of fractures
        }

    def tick(self):
        # Set fracture incidence based on age
        if 1 <= self.age <= 3:  # Toddler age range
            self.properties["fracture_incidence"] = 5  # Arbitrary value for toddlers
        elif 8 <= self.age <= 14:  # Age range for peak incidence in reference text
            self.properties["fracture_incidence"] = 10  # Arbitrary value for peak incidence
        else:
            self.properties["fracture_incidence"] = 1  # Low incidence for other ages

    def makeDescriptionStr(self):
        return f"{self.name}, age {self.age}, has a fracture incidence of {self.properties['fracture_incidence']}."

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
        toddler = Child("Toddler", 2)  # A toddler
        pre_teen = Child("Pre-Teen", 10)  # A pre-teen
        adult = Child("Adult", 20)  # An adult
        world.addObject(toddler)
        world.addObject(pre_teen)
        world.addObject(adult)
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

    # Check the incidence of fractures for toddlers
    toddler_incidence = simulation.rootObject.contains[0].properties["fracture_incidence"]
    pre_teen_incidence = simulation.rootObject.contains[1].properties["fracture_incidence"]

    if toddler_incidence > pre_teen_incidence:
        print("Claim Supported: The peak incidence of fractures occurs in toddlers.")
    else:
        print("Claim Refuted: The peak incidence of fractures does not occur in toddlers.")

if __name__ == "__main__":
    main()
