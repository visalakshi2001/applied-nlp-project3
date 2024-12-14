
# Claim: Inhibiting focal adhesion formation enables cells to convert mechanical strain into eventual scarring.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, focal_adhesion_active=True, mechanical_strain=0, scarring=0):
        super().__init__(name)
        self.properties = {
            "focal_adhesion_active": focal_adhesion_active,
            "mechanical_strain": mechanical_strain,
            "scarring": scarring
        }

    def apply_mechanical_strain(self, strain):
        self.properties["mechanical_strain"] += strain
        if not self.properties["focal_adhesion_active"]:
            self.properties["scarring"] += self.properties["mechanical_strain"] * 0.5  # Arbitrary conversion factor

    def inhibit_focal_adhesion(self):
        self.properties["focal_adhesion_active"] = False

    def makeDescriptionStr(self):
        description = (f"A {self.name} with focal adhesion {'active' if self.properties['focal_adhesion_active'] else 'inactive'}, "
                       f"mechanical strain of {self.properties['mechanical_strain']}, and scarring level of {self.properties['scarring']}.")
        return description

class World(Container):
    def __init__(self):
        super().__init__("cellular environment")

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
        cell = Cell("fibroblast")
        world.addObject(cell)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        for obj in allObjects:
            self.addAction(f"apply mechanical strain to {obj.name}", ["apply_strain", obj])
            self.addAction(f"inhibit focal adhesion of {obj.name}", ["inhibit_focal_adhesion", obj])

    def actionApplyStrain(self, cell):
        if type(cell) != Cell:
            return f"Cannot apply strain to {cell.name}."
        else:
            cell.apply_mechanical_strain(10)  # Arbitrary strain value
            return f"You applied mechanical strain to {cell.name}."

    def actionInhibitFocalAdhesion(self, cell):
        if type(cell) != Cell:
            return f"Cannot inhibit focal adhesion of {cell.name}."
        else:
            cell.inhibit_focal_adhesion()
            return f"You inhibited focal adhesion of {cell.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply_strain":
            self.observationStr = self.actionApplyStrain(action[1])
        elif actionVerb == "inhibit_focal_adhesion":
            self.observationStr = self.actionInhibitFocalAdhesion(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Perform actions to test the claim
    actions = ["inhibit focal adhesion of fibroblast", "apply mechanical strain to fibroblast", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the scarring level after actions
    fibroblast = simulation.rootObject.contains[0]
    if fibroblast.properties["scarring"] > 0:
        print("Claim Supported: Inhibiting focal adhesion formation enables cells to convert mechanical strain into eventual scarring.")
    else:
        print("Claim Refuted: Inhibiting focal adhesion formation does not enable cells to convert mechanical strain into eventual scarring.")

if __name__ == "__main__":
    main()
