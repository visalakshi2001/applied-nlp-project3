
# Claim: Gastric infection with Helicobacter pylori increases risk of gastric cancer in humans.
# The simulation will model the relationship between Helicobacter pylori infection and gastric cancer risk.

from simulation_utils import GameObject, Container

class Infection(GameObject):
    def __init__(self, name, is_infected=False):
        super().__init__(name)
        self.is_infected = is_infected
        self.cancer_risk = 1.0  # Base risk of cancer without infection

    def tick(self):
        if self.is_infected:
            self.cancer_risk *= 2.77  # Increase risk if infected (odds ratio from the study)

    def makeDescriptionStr(self):
        infection_status = "infected" if self.is_infected else "not infected"
        return f"{self.name} is {infection_status} with a cancer risk of {self.cancer_risk:.2f}."

class Patient(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.infection = Infection(name="Helicobacter pylori infection")

    def makeDescriptionStr(self):
        return f"{self.name} has {self.infection.makeDescriptionStr()}"

class World(Container):
    def __init__(self):
        super().__init__("Gastric Environment")
        self.patient = Patient("Patient 1")
        self.addObject(self.patient)

    def makeDescriptionStr(self):
        return f"In the {self.name}, you see: \n\t{self.patient.makeDescriptionStr()}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "infect patient": ["infect", self.rootObject.patient.infection],
            "remove infection": ["remove", self.rootObject.patient.infection]
        }

    def actionInfect(self, infection):
        infection.is_infected = True
        return f"The patient is now infected with Helicobacter pylori."

    def actionRemove(self, infection):
        infection.is_infected = False
        return f"The patient is no longer infected with Helicobacter pylori."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "infect":
            self.observationStr = self.actionInfect(action[1])
        elif actionVerb == "remove":
            self.observationStr = self.actionRemove(action[1])

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        self.rootObject.patient.infection.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["infect patient", "look", "remove infection", "look"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
