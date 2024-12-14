
# Claim: Cnn1 recruitment varies with cell cycle timing.
# The simulation will model the behavior of Cnn1 during different phases of the cell cycle.

from simulation_utils import GameObject, Container

class Cnn1(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "activity_level": 0,  # Represents the activity level of Cnn1
            "cell_cycle_phase": "G1"  # Initial phase of the cell cycle
        }

    def tick(self):
        # Update Cnn1 activity based on the current cell cycle phase
        if self.properties["cell_cycle_phase"] == "G1":
            self.properties["activity_level"] = 1  # Low activity in G1
        elif self.properties["cell_cycle_phase"] == "S":
            self.properties["activity_level"] = 2  # Moderate activity in S
        elif self.properties["cell_cycle_phase"] == "G2":
            self.properties["activity_level"] = 3  # Higher activity in G2
        elif self.properties["cell_cycle_phase"] == "M":
            self.properties["activity_level"] = 5  # Peak activity in M (anaphase)

    def change_phase(self, new_phase):
        self.properties["cell_cycle_phase"] = new_phase

    def makeDescriptionStr(self):
        description = f"{self.name} is currently in the {self.properties['cell_cycle_phase']} phase with an activity level of {self.properties['activity_level']}."
        return description

class CellCycle(Container):
    def __init__(self):
        super().__init__("Cell Cycle")
        self.cnn1 = Cnn1("Cnn1 Protein")
        self.addObject(self.cnn1)

    def simulate_cycle(self):
        phases = ["G1", "S", "G2", "M"]
        results = []
        for phase in phases:
            self.cnn1.change_phase(phase)
            self.cnn1.tick()
            results.append((phase, self.cnn1.properties["activity_level"]))
        return results

class Simulation:
    def __init__(self):
        self.rootObject = CellCycle()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def run_simulation(self):
        cycle_results = self.rootObject.simulate_cycle()
        return cycle_results

def main():
    simulation = Simulation()
    results = simulation.run_simulation()
    
    # Print the results of the simulation
    for phase, activity in results:
        print(f"Phase: {phase}, Cnn1 Activity Level: {activity}")

    # Determine if the claim is supported or refuted
    # The claim states that Cnn1 recruitment varies with cell cycle timing
    # We expect activity levels to change across different phases
    if results[0][1] < results[1][1] < results[2][1] < results[3][1]:
        print("Claim Supported: Cnn1 recruitment varies with cell cycle timing.")
    else:
        print("Claim Refuted: Cnn1 recruitment does not vary with cell cycle timing.")

if __name__ == "__main__":
    main()
