
# Claim: Piezo1 channels are sensors for cell migration in epithelial cells.
# The simulation will test the interaction between TFF1 and Piezo1 and its effect on cell migration.

from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, piezo1_expression=0, tff1_expression=0, mobility=0):
        super().__init__(name)
        self.properties = {
            "piezo1_expression": piezo1_expression,
            "tff1_expression": tff1_expression,
            "mobility": mobility
        }

    def tick(self):
        # Mobility is influenced by the expression of TFF1 and Piezo1
        self.properties["mobility"] = self.properties["tff1_expression"] * (1 + self.properties["piezo1_expression"])

    def makeDescriptionStr(self):
        description = (f"A {self.name} cell with Piezo1 expression level {self.properties['piezo1_expression']}, "
                       f"TFF1 expression level {self.properties['tff1_expression']}, "
                       f"resulting in mobility level {self.properties['mobility']}.")
        return description

class Simulation(Container):
    def __init__(self):
        super().__init__("cell_migration_simulation")
        self.cell = Cell("epithelial")
        self.addObject(self.cell)

    def simulate_interaction(self):
        # Initial state with low expression of Piezo1 and TFF1
        self.cell.properties["piezo1_expression"] = 0.2
        self.cell.properties["tff1_expression"] = 0.5
        self.cell.tick()
        initial_mobility = self.cell.properties["mobility"]

        # Simulate the effect of TFF1 binding to Piezo1
        self.cell.properties["tff1_expression"] = 1.0  # Restoring TFF1 expression
        self.cell.tick()
        restored_mobility = self.cell.properties["mobility"]

        return initial_mobility, restored_mobility

def main():
    simulation = Simulation()
    initial_mobility, restored_mobility = simulation.simulate_interaction()
    
    print(f"Initial Mobility: {initial_mobility}")
    print(f"Restored Mobility: {restored_mobility}")

    # Determine if the claim is supported or refuted
    if restored_mobility > initial_mobility:
        print("Claim Supported: Piezo1 channels are sensors for cell migration in epithelial cells.")
    else:
        print("Claim Refuted: Piezo1 channels are not sensors for cell migration in epithelial cells.")

if __name__ == "__main__":
    main()
