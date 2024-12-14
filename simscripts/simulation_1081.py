
# Claim: Side effects associated with antidepressants do not represent a mortality risk to postmenopausal women.
# The simulation will evaluate the mortality risk associated with different classes of antidepressants.

from simulation_utils import GameObject, Container

class Antidepressant(GameObject):
    def __init__(self, name, mortality_risk):
        super().__init__(name)
        self.properties = {
            "mortality_risk": mortality_risk  # Represents the adjusted hazard ratio for all-cause mortality
        }

    def makeDescriptionStr(self):
        return f"{self.name} with a mortality risk of {self.properties['mortality_risk']}."

class Patient(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.antidepressants = []

    def addAntidepressant(self, antidepressant):
        self.antidepressants.append(antidepressant)

    def calculateTotalMortalityRisk(self):
        total_risk = sum([antidepressant.properties['mortality_risk'] for antidepressant in self.antidepressants])
        return total_risk

class World(Container):
    def __init__(self):
        super().__init__("environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        patient = Patient("postmenopausal_woman")
        
        # Adding different classes of antidepressants with their associated mortality risks
        ssri = Antidepressant("Selective Serotonin Reuptake Inhibitor", 1.066)  # 10.61% risk
        other_ad = Antidepressant("Other Antidepressants", 1.1143)  # 11.43% risk
        tricyclic = Antidepressant("Tricyclic Antidepressants", 1.0812)  # 8.12% risk
        
        patient.addAntidepressant(ssri)
        patient.addAntidepressant(other_ad)
        world.addObject(patient)
        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "calculate mortality risk": ["calculate"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif action[0] == "calculate":
            patient = self.rootObject.contains[0]  # Assuming the first object is the patient
            total_risk = patient.calculateTotalMortalityRisk()
            self.observationStr = f"Total mortality risk for the patient is {total_risk:.2f}."
        
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["look", "calculate mortality risk"]
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
