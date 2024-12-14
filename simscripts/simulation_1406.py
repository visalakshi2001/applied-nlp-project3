
# Claim: β-sheet opening occurs during pleurotolysin pore formation.
# The simulation will model the conformational changes in the MACPF domain of Pleurotolysin during pore formation.

from simulation_utils import GameObject, Container

class Pleurotolysin(GameObject):
    def __init__(self, name, beta_sheet_angle=0):
        super().__init__(name)
        self.properties = {
            "beta_sheet_angle": beta_sheet_angle,  # Angle of the beta-sheet opening
            "is_pore_formed": False  # Indicates if the pore has been formed
        }

    def tick(self):
        # Simulate the opening of the beta-sheet
        if self.properties["beta_sheet_angle"] < 70:
            self.properties["beta_sheet_angle"] += 10  # Increment the angle
        if self.properties["beta_sheet_angle"] >= 70:
            self.properties["is_pore_formed"] = True  # Pore formation is complete

    def makeDescriptionStr(self):
        description = f"{self.name} has a beta-sheet angle of {self.properties['beta_sheet_angle']} degrees."
        if self.properties["is_pore_formed"]:
            description += " The pore has been formed."
        else:
            description += " The pore has not been formed yet."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        pleurotolysin = Pleurotolysin("Pleurotolysin")
        world.addObject(pleurotolysin)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "tick": ["tick"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "tick":
            # Perform a tick to simulate the opening of the beta-sheet
            pleurotolysin = self.rootObject.contains[0]  # Get the Pleurotolysin object
            pleurotolysin.tick()
            self.observationStr = pleurotolysin.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate the process of beta-sheet opening
    for _ in range(8):  # Simulate 8 ticks to ensure the beta-sheet opens
        obs = simulation.step("tick")
        print(obs)

    # Final check to determine if the claim is supported or refuted
    pleurotolysin = simulation.rootObject.contains[0]
    if pleurotolysin.properties["is_pore_formed"]:
        print("Claim Supported: β-sheet opening occurs during pleurotolysin pore formation.")
    else:
        print("Claim Refuted: β-sheet opening does not occur during pleurotolysin pore formation.")

if __name__ == "__main__":
    main()
