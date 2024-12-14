
# Claim: miR-142-5P is a temperature-sensitive microRNA (miRNA).
# The simulation will demonstrate the relationship between RBM3 expression and the expression of miR-142-5p at different temperatures.

from simulation_utils import GameObject, Container

class MicroRNA(GameObject):
    def __init__(self, name, temperature_sensitive=False):
        super().__init__(name)
        self.properties = {
            "temperature_sensitive": temperature_sensitive,
            "expression_level": 0
        }

    def tick(self, rbm3_expression):
        # If RBM3 expression is low, increase miRNA expression level
        if rbm3_expression < 1:
            self.properties["expression_level"] += 1  # Increase expression level
        else:
            self.properties["expression_level"] = max(0, self.properties["expression_level"] - 1)  # Decrease expression level

    def makeDescriptionStr(self):
        description = f"{self.name} (Temperature-sensitive: {self.properties['temperature_sensitive']}, Expression level: {self.properties['expression_level']})"
        return description

class RBM3(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "expression_level": 1  # Normal expression level
        }

    def tick(self, fever):
        # If fever is present, reduce RBM3 expression
        if fever:
            self.properties["expression_level"] = max(0, self.properties["expression_level"] - 1)  # Decrease expression level

    def makeDescriptionStr(self):
        return f"{self.name} (Expression level: {self.properties['expression_level']})"

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
        rbm3 = RBM3("RBM3")
        mir1425p = MicroRNA("miR-142-5p", temperature_sensitive=True)
        world.addObject(rbm3)
        world.addObject(mir1425p)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "simulate fever": ["simulate", True],
            "simulate normal temperature": ["simulate", False]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "simulate":
            fever = action[1]
            rbm3 = self.rootObject.contains[0]  # RBM3
            mir1425p = self.rootObject.contains[1]  # miR-142-5p

            rbm3.tick(fever)  # Update RBM3 based on fever
            mir1425p.tick(rbm3.properties["expression_level"])  # Update miR-142-5p based on RBM3 expression

        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["simulate fever", "simulate normal temperature"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
