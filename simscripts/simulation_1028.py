
# Claim: Reduced responsiveness to interleukin-2 in regulatory T cells is associated with autoimmune diseases such as Type 1 Diabetes.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class RegulatoryTCell(GameObject):
    def __init__(self, name, il2_responsiveness=100, foxp3_expression=100):
        super().__init__(name)
        self.properties = {
            "il2_responsiveness": il2_responsiveness,  # Initial IL-2 responsiveness
            "foxp3_expression": foxp3_expression        # Initial FOXP3 expression
        }

    def tick(self):
        # Simulate the effect of an autoimmune disease on IL-2 responsiveness and FOXP3 expression
        if self.properties["il2_responsiveness"] > 50:
            self.properties["il2_responsiveness"] -= 20  # Reduced responsiveness
            self.properties["foxp3_expression"] -= 10     # Reduced FOXP3 expression

    def makeDescriptionStr(self):
        description = f"A {self.name} with IL-2 responsiveness of {self.properties['il2_responsiveness']} and FOXP3 expression of {self.properties['foxp3_expression']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("immune_system")
        t_cell = RegulatoryTCell("regulatory_T_cell")
        world.addObject(t_cell)        
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

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"simulate autoimmune effect on {objReferent}", ["simulate", obj])

    def actionSimulate(self, t_cell):
        if type(t_cell) != RegulatoryTCell:
            return f"Cannot simulate effects on {t_cell.name}."
        else:
            t_cell.tick()
            return f"Simulated autoimmune effects on {t_cell.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "simulate"):
            self.observationStr = self.actionSimulate(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["simulate autoimmune effect on regulatory_T_cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check on IL-2 responsiveness and FOXP3 expression
    t_cell = simulation.rootObject.contains[0]  # Get the regulatory T cell
    if t_cell.properties["il2_responsiveness"] < 50 and t_cell.properties["foxp3_expression"] < 100:
        print("Claim Supported: Reduced responsiveness to interleukin-2 in regulatory T cells is associated with autoimmune diseases such as Type 1 Diabetes.")
    else:
        print("Claim Refuted: No significant reduction in IL-2 responsiveness in regulatory T cells.")

if __name__ == "__main__":
    main()
