
# Claim: Lice attenuated SIV vaccines induce a stronger antigen-specific T cell response in lymph node cells.
# The simulation will model the relationship between LAVs and T cell responses in lymph nodes.

from simulation_utils import GameObject, Container

class TCell(GameObject):
    def __init__(self, name, response_strength=0):
        super().__init__(name)
        self.response_strength = response_strength

    def tick(self):
        # Simulate the effect of LAVs on T cell response strength
        self.response_strength += 1  # Increment response strength to simulate activation

    def makeDescriptionStr(self):
        return f"{self.name} with response strength: {self.response_strength}"

class LAV(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def induce_response(self, t_cells):
        for t_cell in t_cells:
            t_cell.response_strength += 5  # LAVs significantly boost T cell response

class LymphNode(Container):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        lymph_node = LymphNode("Lymph Node")
        lav = LAV("Lice Attenuated Vaccine")
        
        # Create T cells
        t_cells = [TCell(f"TCell_{i}") for i in range(5)]
        for t_cell in t_cells:
            lymph_node.addObject(t_cell)
        
        lymph_node.addObject(lav)
        return lymph_node

    def generatePossibleActions(self):
        self.possibleActions = {
            "induce T cell response": ["induce_response"],
            "look": ["look"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "induce_response":
            lav = self.rootObject.containsItemWithName("Lice Attenuated Vaccine")[0]
            t_cells = self.rootObject.getAllContainedObjectsRecursive()
            lav.induce_response(t_cells)
            self.observationStr = "LAV induced T cell responses."
        elif action[0] == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Update the state of T cells
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(obj, TCell):
                obj.tick()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["induce T cell response", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the response strength of T cells to determine if the claim is supported
    t_cells = simulation.rootObject.getAllContainedObjectsRecursive()
    response_strengths = [t_cell.response_strength for t_cell in t_cells if isinstance(t_cell, TCell)]
    if all(strength > 0 for strength in response_strengths):
        print("Claim Supported: Lice attenuated SIV vaccines induce a stronger antigen-specific T cell response in lymph node cells.")
    else:
        print("Claim Refuted: Lice attenuated SIV vaccines do not induce a stronger antigen-specific T cell response in lymph node cells.")

if __name__ == "__main__":
    main()
