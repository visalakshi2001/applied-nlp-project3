
# Claim: Immune responses in immune cells are geographically segregated.
# The simulation will model immune cells and their responses to demonstrate geographical segregation.

from simulation_utils import GameObject, Container

class ImmuneCell(GameObject):
    def __init__(self, name, response_type):
        super().__init__(name)
        self.response_type = response_type  # 'pro-inflammatory' or 'anti-inflammatory'
        self.properties = {
            "response": response_type
        }

    def makeDescriptionStr(self):
        return f"{self.name} with a {self.response_type} response."

class Granuloma(Container):
    def __init__(self, name):
        super().__init__(name)

    def segregateResponses(self):
        pro_inflammatory_cells = [cell for cell in self.contains if cell.response_type == 'pro-inflammatory']
        anti_inflammatory_cells = [cell for cell in self.contains if cell.response_type == 'anti-inflammatory']
        return pro_inflammatory_cells, anti_inflammatory_cells

class World(Container):
    def __init__(self):
        super().__init__("granuloma environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.pro_inflammatory_cells, self.anti_inflammatory_cells = self.rootObject.segregateResponses()

    def _initialize_simulation(self):
        world = World()
        granuloma = Granuloma("granuloma")

        # Adding immune cells with different responses
        cell1 = ImmuneCell("Immune Cell 1", "pro-inflammatory")
        cell2 = ImmuneCell("Immune Cell 2", "pro-inflammatory")
        cell3 = ImmuneCell("Immune Cell 3", "anti-inflammatory")
        cell4 = ImmuneCell("Immune Cell 4", "anti-inflammatory")

        granuloma.addObject(cell1)
        granuloma.addObject(cell2)
        granuloma.addObject(cell3)
        granuloma.addObject(cell4)

        world.addObject(granuloma)
        return world

    def checkSegregation(self):
        if self.pro_inflammatory_cells and self.anti_inflammatory_cells:
            return "Supported: Immune responses are geographically segregated."
        else:
            return "Refuted: Immune responses are not segregated."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    segregation_result = simulation.checkSegregation()
    print(segregation_result)

if __name__ == "__main__":
    main()
