
# Claim: One in five surgical randomized controlled trials are discontinued early.
# The simulation will check the rate of early discontinuation of surgical randomized controlled trials.

from simulation_utils import GameObject, Container

class SurgicalTrial(GameObject):
    def __init__(self, trial_id, status):
        super().__init__(trial_id)
        self.status = status  # 'completed' or 'discontinued'

class SurgicalTrialDatabase(Container):
    def __init__(self):
        super().__init__("Surgical Trial Database")
        self.total_trials = 0
        self.discontinued_trials = 0

    def add_trial(self, trial):
        self.addObject(trial)
        self.total_trials += 1
        if trial.status == 'discontinued':
            self.discontinued_trials += 1

    def calculate_discontinuation_rate(self):
        if self.total_trials == 0:
            return 0
        return (self.discontinued_trials / self.total_trials) * 100

class Simulation:
    def __init__(self):
        self.database = self._initialize_simulation()
        self.discontinuation_rate = self.database.calculate_discontinuation_rate()

    def _initialize_simulation(self):
        db = SurgicalTrialDatabase()
        # Simulating 395 trials, with 81 discontinued (21%)
        for i in range(395):
            if i < 81:  # First 81 trials are discontinued
                trial = SurgicalTrial(f"Trial_{i+1}", 'discontinued')
            else:
                trial = SurgicalTrial(f"Trial_{i+1}", 'completed')
            db.add_trial(trial)
        return db

    def get_result(self):
        if self.discontinuation_rate >= 20:
            return "Supported: The claim that one in five surgical randomized controlled trials are discontinued early is true."
        else:
            return "Refuted: The claim that one in five surgical randomized controlled trials are discontinued early is false."

def main():
    simulation = Simulation()
    result = simulation.get_result()
    print(result)

if __name__ == "__main__":
    main()
