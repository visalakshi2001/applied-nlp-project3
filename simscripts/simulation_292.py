
# Claim: Cost effectiveness evaluations based on cRCT data lack external validity.
# The simulation will evaluate the external validity of cost-effectiveness analyses based on RCT data versus observational data.

from simulation_utils import GameObject, Container

class CostEffectivenessAnalysis(GameObject):
    def __init__(self, name, based_on_rct=True, external_validity=False):
        super().__init__(name)
        self.properties = {
            "based_on_rct": based_on_rct,
            "external_validity": external_validity
        }

    def evaluate(self):
        if self.properties["based_on_rct"]:
            # If based on RCT, we assume it lacks external validity
            self.properties["external_validity"] = False
        else:
            # If based on observational data, we assume it has external validity
            self.properties["external_validity"] = True

    def makeDescriptionStr(self):
        validity = "valid" if self.properties["external_validity"] else "invalid"
        return f"{self.name} is based on RCT: {self.properties['based_on_rct']}, external validity: {validity}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("Cost Effectiveness Evaluation Environment")
        rct_analysis = CostEffectivenessAnalysis("RCT Based Analysis", based_on_rct=True)
        observational_analysis = CostEffectivenessAnalysis("Observational Data Analysis", based_on_rct=False)
        
        world.addObject(rct_analysis)
        world.addObject(observational_analysis)
        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "evaluate": ["evaluate"]
        }

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "evaluate":
            for obj in self.rootObject.contains:
                obj.evaluate()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Evaluate the analyses
    result = simulation.step("evaluate")
    print(result)

    # Determine if the claim is supported or refuted
    rct_analysis = simulation.rootObject.contains[0]
    if not rct_analysis.properties["external_validity"]:
        print("Claim Supported: Cost effectiveness evaluations based on cRCT data lack external validity.")
    else:
        print("Claim Refuted: Cost effectiveness evaluations based on cRCT data do not lack external validity.")

if __name__ == "__main__":
    main()
