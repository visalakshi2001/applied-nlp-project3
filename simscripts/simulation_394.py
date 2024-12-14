
# Claim: Excess gestational weight gain is associated with obesity-related pregnancy outcomes.
# The simulation will evaluate the impact of dietary and lifestyle interventions on gestational weight gain and pregnancy outcomes.

from simulation_utils import GameObject, Container

class Intervention(GameObject):
    def __init__(self, name, weight_gain_reduction):
        super().__init__(name)
        self.weight_gain_reduction = weight_gain_reduction  # kg reduction in gestational weight gain

class PregnancyOutcome(GameObject):
    def __init__(self, name, pre_eclampsia_risk, shoulder_dystocia_risk):
        super().__init__(name)
        self.pre_eclampsia_risk = pre_eclampsia_risk  # relative risk
        self.shoulder_dystocia_risk = shoulder_dystocia_risk  # relative risk

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.evaluate_outcomes()

    def _initialize_simulation(self):
        world = Container("Pregnancy Environment")
        
        # Interventions with their respective weight gain reductions
        dietary_intervention = Intervention("Dietary Intervention", 3.84)  # kg
        physical_activity_intervention = Intervention("Physical Activity", 1.42)  # kg
        
        # Pregnancy outcomes based on interventions
        outcome_dietary = PregnancyOutcome("Dietary Outcome", 0.74, 0.39)  # relative risks
        outcome_physical_activity = PregnancyOutcome("Physical Activity Outcome", 0.85, 0.66)  # relative risks
        
        world.addObject(dietary_intervention)
        world.addObject(physical_activity_intervention)
        world.addObject(outcome_dietary)
        world.addObject(outcome_physical_activity)
        
        return world

    def evaluate_outcomes(self):
        # Check the outcomes based on interventions
        dietary_intervention = self.rootObject.containsItemWithName("Dietary Intervention")[0]
        outcome_dietary = self.rootObject.containsItemWithName("Dietary Outcome")[0]
        
        # If dietary intervention reduces weight gain and improves outcomes
        if dietary_intervention.weight_gain_reduction > 0 and outcome_dietary.pre_eclampsia_risk < 1:
            self.result = "Supported"
        else:
            self.result = "Refuted"

    def makeDescriptionStr(self):
        return f"In the {self.rootObject.name}, the claim is: {self.result}"

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
