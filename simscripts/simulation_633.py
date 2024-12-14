
# Claim: Inhibiting focal adhesion formation increases the rate at which cells convert mechanical strain into inflammation and fibrosis.
# The simulation will model the effects of inhibiting focal adhesion kinase (FAK) on inflammation and fibrosis in a controlled environment.

from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, focal_adhesion_active=True):
        super().__init__(name)
        self.focal_adhesion_active = focal_adhesion_active
        self.inflammation_level = 0
        self.fibrosis_level = 0

    def apply_mechanical_strain(self):
        if not self.focal_adhesion_active:
            self.inflammation_level += 2  # Increased inflammation due to inhibition
            self.fibrosis_level += 2       # Increased fibrosis due to inhibition
        else:
            self.inflammation_level += 1    # Normal inflammation response
            self.fibrosis_level += 1        # Normal fibrosis response

    def makeDescriptionStr(self):
        return f"{self.name}: Inflammation Level: {self.inflammation_level}, Fibrosis Level: {self.fibrosis_level}, Focal Adhesion Active: {self.focal_adhesion_active}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell_environment")
        active_cell = Cell("Active Cell", focal_adhesion_active=True)
        inhibited_cell = Cell("Inhibited Cell", focal_adhesion_active=False)
        world.addObject(active_cell)
        world.addObject(inhibited_cell)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "apply mechanical strain to Active Cell": ["apply", self.rootObject.contains[0]],
            "apply mechanical strain to Inhibited Cell": ["apply", self.rootObject.contains[1]],
            "look": ["look"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply":
            action[1].apply_mechanical_strain()
            self.observationStr = f"Applied mechanical strain to {action[1].name}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["apply mechanical strain to Active Cell", "apply mechanical strain to Inhibited Cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final observation to determine if the claim is supported or refuted
    inhibited_cell = simulation.rootObject.contains[1]
    if inhibited_cell.inflammation_level > 1 and inhibited_cell.fibrosis_level > 1:
        print("Claim Supported: Inhibiting focal adhesion formation increases inflammation and fibrosis.")
    else:
        print("Claim Refuted: Inhibiting focal adhesion formation does not increase inflammation and fibrosis.")

if __name__ == "__main__":
    main()
