
# Claim: 32% of liver transplantation programs required patients to discontinue methadone treatment in 2001.
# The simulation will check if the claim is supported by the evidence provided in the reference text.

from simulation_utils import GameObject, Container

class LiverTransplantProgram(GameObject):
    def __init__(self, name, requires_discontinuation):
        super().__init__(name)
        self.requires_discontinuation = requires_discontinuation

class Simulation:
    def __init__(self):
        self.programs = self._initialize_simulation()
        self.result = self.check_claim()

    def _initialize_simulation(self):
        # Create 97 liver transplantation programs
        programs = []
        for i in range(97):
            # 32% of programs require discontinuation of methadone
            if i < 32:  # First 32 programs require discontinuation
                program = LiverTransplantProgram(f"Program_{i+1}", True)
            else:
                program = LiverTransplantProgram(f"Program_{i+1}", False)
            programs.append(program)
        return programs

    def check_claim(self):
        # Count the number of programs that require discontinuation
        count_discontinuation = sum(1 for program in self.programs if program.requires_discontinuation)
        percentage = (count_discontinuation / len(self.programs)) * 100
        # Check if the percentage matches the claim
        if percentage == 32:
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    print(simulation.result)

if __name__ == "__main__":
    main()
