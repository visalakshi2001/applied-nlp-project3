
# Claim: miR-142-5P is a known regulator of raised body temperature.
# The simulation will test the relationship between miR-142-5P and body temperature regulation.

from simulation_utils import GameObject, Container

class MiRNA(GameObject):
    def __init__(self, name, expression_level=0):
        super().__init__(name)
        self.properties = {
            "expression_level": expression_level
        }

    def tick(self):
        # Simulate the effect of temperature on miRNA expression
        if self.name == "miR-142-5P":
            # Increase expression level when temperature is high
            self.properties["expression_level"] += 1

    def makeDescriptionStr(self):
        return f"{self.name} with expression level: {self.properties['expression_level']}"

class Temperature(GameObject):
    def __init__(self, name, level=37):
        super().__init__(name)
        self.properties = {
            "level": level  # Normal body temperature in Celsius
        }

    def increase(self):
        self.properties["level"] += 1

    def decrease(self):
        self.properties["level"] -= 1

    def makeDescriptionStr(self):
        return f"Temperature: {self.properties['level']} °C"

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
        temperature = Temperature("Body Temperature", 37)  # Normal temperature
        mirna = MiRNA("miR-142-5P")
        world.addObject(temperature)
        world.addObject(mirna)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("increase temperature", ["increase"])
        self.addAction("decrease temperature", ["decrease"])
        self.addAction("look", ["look"])

    def actionIncrease(self, temperature):
        temperature.increase()
        return f"You increase the {temperature.name} by 1 °C."

    def actionDecrease(self, temperature):
        temperature.decrease()
        return f"You decrease the {temperature.name} by 1 °C."

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
            temp = self.rootObject.contains[0]  # Assuming the first object is temperature
            self.observationStr = self.actionIncrease(temp)
        elif actionVerb == "decrease":
            temp = self.rootObject.contains[0]  # Assuming the first object is temperature
            self.observationStr = self.actionDecrease(temp)

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
    actions = ["increase temperature", "increase temperature", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the expression level of miR-142-5P after temperature increases
    mirna = simulation.rootObject.contains[1]  # Assuming the second object is miR-142-5P
    if mirna.properties["expression_level"] > 0:
        print("Claim Supported: miR-142-5P is a known regulator of raised body temperature.")
    else:
        print("Claim Refuted: miR-142-5P is not a known regulator of raised body temperature.")

if __name__ == "__main__":
    main()
