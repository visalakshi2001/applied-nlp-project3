
# Claim: Bariatric surgery leads to positive outcomes in mental health.
# This simulation will evaluate the impact of bariatric surgery on mental health outcomes, specifically depression.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, has_bariatric_surgery=False, depression_level=100):
        super().__init__(name)
        self.properties = {
            "has_bariatric_surgery": has_bariatric_surgery,
            "depression_level": depression_level  # 0 = no depression, 100 = severe depression
        }

    def undergo_bariatric_surgery(self):
        self.properties["has_bariatric_surgery"] = True
        # Simulate the effect of surgery on depression
        self.properties["depression_level"] = max(0, self.properties["depression_level"] - 50)  # Decrease depression level

    def makeDescriptionStr(self):
        return f"{self.name} has {'undergone' if self.properties['has_bariatric_surgery'] else 'not undergone'} bariatric surgery. Current depression level: {self.properties['depression_level']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hospital")
        patient1 = Patient("Patient A", has_bariatric_surgery=False, depression_level=80)
        patient2 = Patient("Patient B", has_bariatric_surgery=True, depression_level=30)
        world.addObject(patient1)
        world.addObject(patient2)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "perform bariatric surgery on Patient A": ["surgery", self.rootObject.contains[0]],  # Patient A
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "surgery":
            patient = action[1]
            patient.undergo_bariatric_surgery()
            self.observationStr = f"{patient.name} has undergone bariatric surgery."
        
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["look", "perform bariatric surgery on Patient A"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
