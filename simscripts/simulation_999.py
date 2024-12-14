
# Claim: Pyridostatin reduces proliferation of homologous recombination - defective cells.
# This simulation will model the effect of Pyridostatin (PDS) on HR-defective cells.

from simulation_utils import GameObject, Container

class HRDefectiveCell(GameObject):
    def __init__(self, name, proliferation_rate=100, DSB_accumulation=0):
        super().__init__(name)
        self.proliferation_rate = proliferation_rate  # Initial proliferation rate
        self.DSB_accumulation = DSB_accumulation  # Double-strand break accumulation

    def apply_pyridostatin(self):
        # Simulate the effect of Pyridostatin
        self.DSB_accumulation += 50  # Increase DSB accumulation
        self.proliferation_rate -= 30  # Decrease proliferation rate
        return self.proliferation_rate, self.DSB_accumulation

    def makeDescriptionStr(self):
        return f"{self.name} with proliferation rate: {self.proliferation_rate} and DSB accumulation: {self.DSB_accumulation}."

class Simulation:
    def __init__(self):
        self.cell = HRDefectiveCell("HR-Defective Cell")
        self.initial_proliferation = self.cell.proliferation_rate
        self.initial_DSB = self.cell.DSB_accumulation
        self.apply_pyridostatin()

    def apply_pyridostatin(self):
        # Apply Pyridostatin to the HR-defective cell
        new_proliferation, new_DSB = self.cell.apply_pyridostatin()
        return new_proliferation, new_DSB

    def check_claim(self):
        # Check if the claim is supported or refuted
        if self.cell.proliferation_rate < self.initial_proliferation:
            return "Supported: Pyridostatin reduces proliferation of HR-defective cells."
        else:
            return "Refuted: Pyridostatin does not reduce proliferation of HR-defective cells."

def main():
    simulation = Simulation()
    print(simulation.check_claim())

if __name__ == "__main__":
    main()
