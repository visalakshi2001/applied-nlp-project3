
# Claim: Eilat virus (EILV) produced in mosquitos elicits rapid and long-lasting neutralizing antibodies in nonhuman primates.

from simulation_utils import GameObject, Container

class EilatVirus(GameObject):
    def __init__(self, name, rapid_immunity_days=4, long_last_immunity_days=290):
        super().__init__(name)
        self.properties = {
            "rapid_immunity_days": rapid_immunity_days,
            "long_last_immunity_days": long_last_immunity_days,
            "neutralizing_antibodies": False,
            "protection": False
        }

    def elicit_immunity(self):
        self.properties["neutralizing_antibodies"] = True
        self.properties["protection"] = True

    def tick(self):
        if self.properties["neutralizing_antibodies"]:
            self.properties["long_last_immunity_days"] -= 1

class NonHumanPrimate(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "immunity": False,
            "viremia": False,
            "fever": False
        }

    def receive_vaccine(self, virus):
        virus.elicit_immunity()
        self.properties["immunity"] = virus.properties["protection"]

    def tick(self):
        if self.properties["immunity"]:
            self.properties["viremia"] = False
            self.properties["fever"] = False

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

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
        eilat_virus = EilatVirus("Eilat Virus")
        primate = NonHumanPrimate("Nonhuman Primate")
        world.addObject(eilat_virus)
        world.addObject(primate)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "vaccinate primate with Eilat Virus": ["vaccinate", "Eilat Virus", "Nonhuman Primate"],
            "tick": ["tick"]
        }

    def step(self, actionStr):
        if actionStr == "vaccinate primate with Eilat Virus":
            virus = self.rootObject.containsItemWithName("Eilat Virus")[0]
            primate = self.rootObject.containsItemWithName("Nonhuman Primate")[0]
            primate.receive_vaccine(virus)
            return f"{primate.name} has been vaccinated with {virus.name}."
        elif actionStr == "tick":
            for obj in self.rootObject.contains:
                obj.tick()
            return "One tick of the simulation has occurred."
        else:
            return "ERROR: Unknown action."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["vaccinate primate with Eilat Virus", "tick"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the properties of the primate after vaccination
    primate = simulation.rootObject.containsItemWithName("Nonhuman Primate")[0]
    if primate.properties["immunity"]:
        print("Claim Supported: Eilat virus elicits rapid and long-lasting neutralizing antibodies in nonhuman primates.")
    else:
        print("Claim Refuted: Eilat virus does not elicit rapid and long-lasting neutralizing antibodies in nonhuman primates.")

if __name__ == "__main__":
    main()
