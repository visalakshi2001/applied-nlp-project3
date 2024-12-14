
# Claim: A country's Vaccine Alliance (GAVI) eligibility is not indicative of accelerated adoption of the Hub vaccine.
# The simulation will analyze the relationship between GAVI eligibility and vaccine adoption speed.

from simulation_utils import GameObject, Container

class Vaccine(GameObject):
    def __init__(self, name, gavi_eligibility=False, adoption_time=0):
        super().__init__(name)
        self.properties = {
            "gavi_eligibility": gavi_eligibility,
            "adoption_time": adoption_time  # Time taken to adopt the vaccine
        }

    def tick(self):
        # Simulate the effect of GAVI eligibility on adoption time
        if self.properties["gavi_eligibility"]:
            self.properties["adoption_time"] *= 0.37  # Speed up adoption if GAVI eligible

    def makeDescriptionStr(self):
        description = f"{self.name} with GAVI eligibility: {self.properties['gavi_eligibility']}, adoption time: {self.properties['adoption_time']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "vaccine adoption environment")

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
        # Create vaccines with and without GAVI eligibility
        vaccine_with_gavi = Vaccine("Hub Vaccine", gavi_eligibility=True, adoption_time=10)  # 10 time units to adopt
        vaccine_without_gavi = Vaccine("Other Vaccine", gavi_eligibility=False, adoption_time=10)  # 10 time units to adopt
        world.addObject(vaccine_with_gavi)
        world.addObject(vaccine_without_gavi)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            # Perform a tick to simulate the passage of time and effects of GAVI eligibility
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the effect of time passing
    for _ in range(1):  # Just one tick to see the effect
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the adoption times to verify the claim
    hub_vaccine = simulation.rootObject.containsItemWithName("Hub Vaccine")[0]
    other_vaccine = simulation.rootObject.containsItemWithName("Other Vaccine")[0]

    if hub_vaccine.properties["adoption_time"] < other_vaccine.properties["adoption_time"]:
        result = "Supported: GAVI eligibility is associated with accelerated adoption."
    else:
        result = "Refuted: GAVI eligibility is not associated with accelerated adoption."

    print(result)

if __name__ == "__main__":
    main()
