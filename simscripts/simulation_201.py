
# Claim: CD28 signals regulate trafficking of murine auto-reactive T cells into target tissues.
# The simulation will model T cells and their trafficking behavior based on CD28 signaling.

from simulation_utils import GameObject, Container

class TCell(GameObject):
    def __init__(self, name, is_auto_reactive=False, cd28_signaling_active=False):
        super().__init__(name)
        self.properties = {
            "is_auto_reactive": is_auto_reactive,
            "cd28_signaling_active": cd28_signaling_active,
            "in_target_tissue": False
        }

    def tick(self):
        # If CD28 signaling is active, allow the T cell to enter target tissues if it's auto-reactive
        if self.properties["cd28_signaling_active"] and self.properties["is_auto_reactive"]:
            self.properties["in_target_tissue"] = True
        else:
            self.properties["in_target_tissue"] = False

    def makeDescriptionStr(self):
        description = f"A T cell named {self.name}, which is {'auto-reactive' if self.properties['is_auto_reactive'] else 'not auto-reactive'} and has {'active' if self.properties['cd28_signaling_active'] else 'inactive'} CD28 signaling. Currently in target tissue: {self.properties['in_target_tissue']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("immune_system")
        auto_reactive_t_cell = TCell("auto_reactive_T_cell", is_auto_reactive=True, cd28_signaling_active=True)
        non_auto_reactive_t_cell = TCell("non_auto_reactive_T_cell", is_auto_reactive=False, cd28_signaling_active=False)
        world.addObject(auto_reactive_t_cell)
        world.addObject(non_auto_reactive_t_cell)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            # Perform a tick to update the state of the T cells
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Perform a tick to see the results of the simulation
    print("Performing tick...")
    result = simulation.step("tick")
    print(result)

    # Check if the auto-reactive T cell is in target tissue
    auto_reactive_t_cell = simulation.rootObject.containsItemWithName("auto_reactive_T_cell")[0]
    if auto_reactive_t_cell.properties["in_target_tissue"]:
        print("Claim Supported: CD28 signals regulate trafficking of murine auto-reactive T cells into target tissues.")
    else:
        print("Claim Refuted: CD28 signals do not regulate trafficking of murine auto-reactive T cells into target tissues.")

if __name__ == "__main__":
    main()
