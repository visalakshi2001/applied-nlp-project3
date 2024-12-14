
# Claim: Anthrax spores are very difficult to dispose once they are dispersed.
# This simulation will model the behavior of anthrax spores in an environment to verify the claim.

from simulation_utils import GameObject, Container

class AnthraxSpore(GameObject):
    def __init__(self, name, dispersed=False):
        super().__init__(name)
        self.properties = {
            "dispersed": dispersed,
            "reaerosolized": False
        }

    def disperse(self):
        self.properties["dispersed"] = True

    def reaerosolize(self):
        if self.properties["dispersed"]:
            self.properties["reaerosolized"] = True

    def makeDescriptionStr(self):
        return f"{self.name} - Dispersed: {self.properties['dispersed']}, Reaerosolized: {self.properties['reaerosolized']}"

class OfficeEnvironment(Container):
    def __init__(self):
        super().__init__("office environment")

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
        environment = OfficeEnvironment()
        anthrax_spore = AnthraxSpore("Anthrax Spore")
        environment.addObject(anthrax_spore)
        return environment

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("disperse anthrax spore", ["disperse"])
        self.addAction("reaerosolize anthrax spore", ["reaerosolize"])
        self.addAction("look", ["look"])

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "disperse":
            anthrax_spore = self.rootObject.contains[0]
            anthrax_spore.disperse()
            self.observationStr = f"You dispersed the {anthrax_spore.name}."
        elif actionVerb == "reaerosolize":
            anthrax_spore = self.rootObject.contains[0]
            anthrax_spore.reaerosolize()
            self.observationStr = f"The {anthrax_spore.name} has been reaerosolized."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["disperse anthrax spore", "reaerosolize anthrax spore", "look"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check if the claim is supported or refuted based on the properties of the anthrax spore
    anthrax_spore = simulation.rootObject.contains[0]
    if anthrax_spore.properties["reaerosolized"]:
        print("Claim Supported: Anthrax spores are very difficult to dispose once they are dispersed.")
    else:
        print("Claim Refuted: Anthrax spores can be disposed of easily.")

if __name__ == "__main__":
    main()
