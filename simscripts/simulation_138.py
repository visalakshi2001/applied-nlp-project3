
# Claim: Asymptomatic visual impairment screening in elderly populations leads to improved vision.
# The simulation will assess whether visual screening leads to improvements in self-reported visual problems.

from simulation_utils import GameObject, Container

class ElderlyPerson(GameObject):
    def __init__(self, name, has_visual_impairment=False):
        super().__init__(name)
        self.properties = {
            "has_visual_impairment": has_visual_impairment,
            "self_reported_visual_problems": 1  # 1 indicates problems, 0 indicates no problems
        }

    def undergo_screening(self):
        # Simulate the effect of screening
        if self.properties["has_visual_impairment"]:
            # Screening does not improve self-reported problems
            self.properties["self_reported_visual_problems"] = 1
        else:
            # No visual impairment, no problems reported
            self.properties["self_reported_visual_problems"] = 0

    def makeDescriptionStr(self):
        return f"{self.name} has visual impairment: {self.properties['has_visual_impairment']}, self-reported visual problems: {self.properties['self_reported_visual_problems']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("community")
        elderly_person1 = ElderlyPerson("Elderly Person 1", has_visual_impairment=True)
        elderly_person2 = ElderlyPerson("Elderly Person 2", has_visual_impairment=False)
        world.addObject(elderly_person1)
        world.addObject(elderly_person2)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"screen": ["screen"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "screen":
            # Perform screening for all elderly persons
            for person in self.rootObject.contains:
                person.undergo_screening()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print("Before screening:")
    print(simulation.observationStr)
    
    print("\nPerforming screening...")
    result = simulation.step("screen")
    print(result)

    # Determine if the claim is supported or refuted
    if "self-reported visual problems: 1" in result:
        verification_result = "Refuted"
    else:
        verification_result = "Supported"

    print(f"\nClaim verification result: {verification_result}")

if __name__ == "__main__":
    main()
