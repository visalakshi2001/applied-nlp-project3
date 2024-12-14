
# Claim: There was an estimated 30 million cases of pneumonia in young children worldwide in 2010.
# The simulation will estimate the number of cases based on the provided reference text.

from simulation_utils import GameObject, Container

class PneumoniaCase(GameObject):
    def __init__(self, severity, count):
        super().__init__(f"{severity} pneumonia case")
        self.properties = {
            "severity": severity,
            "count": count
        }

    def makeDescriptionStr(self):
        return f"A {self.properties['severity']} pneumonia case with a count of {self.properties['count']}."

class PneumoniaSimulation(Container):
    def __init__(self):
        super().__init__("Pneumonia Simulation Environment")
        self.addObject(PneumoniaCase("severe", 11.9))  # in millions
        self.addObject(PneumoniaCase("very severe", 3.0))  # in millions

    def total_cases(self):
        total = sum(case.properties['count'] for case in self.contains)
        return total

def main():
    simulation = PneumoniaSimulation()
    total_cases = simulation.total_cases() * 1e6  # Convert millions to actual count
    print(f"Total estimated pneumonia cases in young children worldwide in 2010: {total_cases}")

    # Claim verification
    claim_cases = 30e6  # 30 million
    if total_cases >= claim_cases:
        print("Claim Supported: The estimated cases of pneumonia in young children worldwide in 2010 is supported.")
    else:
        print("Claim Refuted: The estimated cases of pneumonia in young children worldwide in 2010 is refuted.")

if __name__ == "__main__":
    main()
