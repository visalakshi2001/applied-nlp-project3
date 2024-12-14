
# Claim: Cholesterol loading induces KLF4 expression in VSMCs, resulting in the expression of pro-inflammatory cytokines.
# The simulation will model the effect of cholesterol on VSMCs and KLF4 expression.

from simulation_utils import GameObject, Container

class VSMC(GameObject):
    def __init__(self, name, cholesterol_level=0, KLF4_expression=0, pro_inflammatory_cytokines=0):
        super().__init__(name)
        self.properties = {
            "cholesterol_level": cholesterol_level,
            "KLF4_expression": KLF4_expression,
            "pro_inflammatory_cytokines": pro_inflammatory_cytokines
        }

    def tick(self):
        # Simulate the effect of cholesterol on KLF4 expression and pro-inflammatory cytokines
        if self.properties["cholesterol_level"] > 0:
            self.properties["KLF4_expression"] += 1  # Increase KLF4 expression with cholesterol
            self.properties["pro_inflammatory_cytokines"] += 2  # Increase cytokines as a response

    def makeDescriptionStr(self):
        description = (f"A {self.name} with cholesterol level {self.properties['cholesterol_level']}, "
                       f"KLF4 expression {self.properties['KLF4_expression']}, "
                       f"and pro-inflammatory cytokines {self.properties['pro_inflammatory_cytokines']}.")
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
        vsmc = VSMC("Vascular Smooth Muscle Cell")
        world.addObject(vsmc)        
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"load cholesterol into {objReferent}", ["load", obj])

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def actionLoadCholesterol(self, vsmc):
        if type(vsmc) != VSMC:
            return f"Cannot load cholesterol into {vsmc.name}."
        else:
            vsmc.properties["cholesterol_level"] += 1
            return f"You load cholesterol into {vsmc.name}."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "load":
            self.observationStr = self.actionLoadCholesterol(action[1])

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
    actions = ["load cholesterol into Vascular Smooth Muscle Cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
