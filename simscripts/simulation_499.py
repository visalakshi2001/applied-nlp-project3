
# Claim: HbA1c consistently overestimates glycemic control in black individuals with Sickle cell trait (SCT).
# The simulation will evaluate the relationship between HbA1c levels and the presence of SCT.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, has_SCT, fasting_glucose):
        super().__init__(name)
        self.has_SCT = has_SCT
        self.fasting_glucose = fasting_glucose
        self.HbA1c = self.calculate_HbA1c()

    def calculate_HbA1c(self):
        # HbA1c levels based on fasting glucose and SCT status
        if self.has_SCT:
            return 5.72 - (0.29 * (self.fasting_glucose - 100) / 100)  # Adjusted for SCT
        else:
            return 6.01 - (0.30 * (self.fasting_glucose - 100) / 100)  # Normal HbA1c

    def makeDescriptionStr(self):
        return f"{self.name} (SCT: {self.has_SCT}, Fasting Glucose: {self.fasting_glucose}, HbA1c: {self.HbA1c:.2f})"

class Study(Container):
    def __init__(self):
        super().__init__("HbA1c Study")
        self.participants = []

    def add_participant(self, participant):
        self.addObject(participant)
        self.participants.append(participant)

    def analyze_results(self):
        SCT_HbA1c = [p.HbA1c for p in self.participants if p.has_SCT]
        non_SCT_HbA1c = [p.HbA1c for p in self.participants if not p.has_SCT]

        mean_SCT_HbA1c = sum(SCT_HbA1c) / len(SCT_HbA1c) if SCT_HbA1c else 0
        mean_non_SCT_HbA1c = sum(non_SCT_HbA1c) / len(non_SCT_HbA1c) if non_SCT_HbA1c else 0

        return mean_SCT_HbA1c, mean_non_SCT_HbA1c

class Simulation:
    def __init__(self):
        self.study = Study()
        self.setup_participants()

    def setup_participants(self):
        # Adding participants with varying fasting glucose levels
        self.study.add_participant(Participant("Participant 1", True, 100))
        self.study.add_participant(Participant("Participant 2", True, 120))
        self.study.add_participant(Participant("Participant 3", False, 100))
        self.study.add_participant(Participant("Participant 4", False, 120))

    def run_analysis(self):
        mean_SCT_HbA1c, mean_non_SCT_HbA1c = self.study.analyze_results()
        print(f"Mean HbA1c for SCT participants: {mean_SCT_HbA1c:.2f}")
        print(f"Mean HbA1c for non-SCT participants: {mean_non_SCT_HbA1c:.2f}")

        if mean_SCT_HbA1c < mean_non_SCT_HbA1c:
            return "Claim Supported: HbA1c underestimates glycemic control in SCT individuals."
        else:
            return "Claim Refuted: HbA1c does not underestimate glycemic control in SCT individuals."

def main():
    simulation = Simulation()
    simulation.run_analysis()

if __name__ == "__main__":
    main()
