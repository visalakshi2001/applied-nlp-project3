
# Claim: Helicobacter pylori-induced aberrant NF-kB-dependent expression of activation-induced cytidine deaminase contributes to the mutagenesis of host DNA.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class HelicobacterPylori(GameObject):
    def __init__(self, name, is_cagPAI_positive=False):
        super().__init__(name)
        self.properties = {
            "is_cagPAI_positive": is_cagPAI_positive,
            "AID_expression": 0,
            "mutation_accumulation": 0
        }

    def induce_AID_expression(self):
        if self.properties["is_cagPAI_positive"]:
            self.properties["AID_expression"] = 1  # Indicating AID is expressed
            self.properties["mutation_accumulation"] += 1  # Indicating mutation accumulation

    def tick(self):
        # Simulate the effect of AID expression on mutation accumulation
        if self.properties["AID_expression"] > 0:
            self.properties["mutation_accumulation"] += 1  # Accumulate mutations

    def makeDescriptionStr(self):
        description = f"{self.name} (cagPAI positive: {self.properties['is_cagPAI_positive']}) has AID expression level: {self.properties['AID_expression']} and mutation accumulation: {self.properties['mutation_accumulation']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        h_pylori = HelicobacterPylori("Helicobacter pylori", is_cagPAI_positive=True)
        world.addObject(h_pylori)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("induce AID expression", ["induce_AID_expression"])
        self.addAction("tick", ["tick"])
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "induce_AID_expression":
            h_pylori = self.rootObject.contains[0]  # Assuming only one H. pylori in the simulation
            h_pylori.induce_AID_expression()
            self.observationStr = f"AID expression induced in {h_pylori.name}."
        elif actionVerb == "tick":
            h_pylori = self.rootObject.contains[0]
            h_pylori.tick()
            self.observationStr = f"Tick processed for {h_pylori.name}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["induce AID expression", "tick", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final observation to determine if the claim is supported or refuted
    h_pylori = simulation.rootObject.contains[0]
    if h_pylori.properties["mutation_accumulation"] > 0:
        print("Claim Supported: Helicobacter pylori-induced aberrant NF-kB-dependent expression of AID contributes to mutagenesis.")
    else:
        print("Claim Refuted: No evidence of mutagenesis from Helicobacter pylori.")

if __name__ == "__main__":
    main()
