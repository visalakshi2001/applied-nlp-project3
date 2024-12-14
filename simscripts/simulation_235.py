
# Claim: Cell autonomous sex determination in somatic cells occurs in Galliformes.
# The simulation will test the inherent sex identity of avian somatic cells.

from simulation_utils import GameObject, Container

class AvianCell(GameObject):
    def __init__(self, name, sex_identity):
        super().__init__(name)
        self.properties = {
            "sex_identity": sex_identity  # 'male' or 'female'
        }

    def makeDescriptionStr(self):
        return f"{self.name} with sex identity: {self.properties['sex_identity']}."

class Gynandromorph(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.cells = {
            "left": AvianCell("Left Cell", "male"),
            "right": AvianCell("Right Cell", "female")
        }

    def makeDescriptionStr(self):
        description = f"{self.name} consists of:\n"
        for side, cell in self.cells.items():
            description += f"\t{cell.makeDescriptionStr()}\n"
        return description

class World(Container):
    def __init__(self):
        super().__init__("environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        gynandromorph = Gynandromorph("Gynandromorph Chicken")
        world.addObject(gynandromorph)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Check the inherent sex identity of the cells
    left_cell_identity = simulation.rootObject.contains[0].cells["left"].properties["sex_identity"]
    right_cell_identity = simulation.rootObject.contains[0].cells["right"].properties["sex_identity"]

    # Determine if the claim is supported or refuted
    if left_cell_identity == "male" and right_cell_identity == "female":
        result = "Supported"
    else:
        result = "Refuted"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
