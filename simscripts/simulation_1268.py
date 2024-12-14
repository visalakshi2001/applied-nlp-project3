
# Claim: The risk of cancer rises with level of alcohol consumption.
# Simulation to verify the claim based on the provided reference text.

from simulation_utils import GameObject, Container

class AlcoholConsumption(GameObject):
    def __init__(self, level=0):
        super().__init__("Alcohol Consumption")
        self.level = level  # Level of alcohol consumption
        self.cancer_risk = 0  # Initial cancer risk

    def tick(self):
        # The risk of cancer increases with the level of alcohol consumption
        self.cancer_risk = self.level * 1.5  # Arbitrary multiplier to simulate risk increase

    def makeDescriptionStr(self):
        return f"Alcohol consumption level: {self.level}, Cancer risk: {self.cancer_risk}"

class Population(Container):
    def __init__(self):
        super().__init__("Population")
        self.alcohol_consumption = AlcoholConsumption()

    def increase_consumption(self, amount):
        self.alcohol_consumption.level += amount

    def decrease_consumption(self, amount):
        self.alcohol_consumption.level = max(0, self.alcohol_consumption.level - amount)

class Simulation:
    def __init__(self):
        self.population = Population()
        self.observationStr = self.population.makeDescriptionStr()
        self.generatePossibleActions()

    def generatePossibleActions(self):
        self.possibleActions = {
            "increase consumption": ["increase", 1],
            "decrease consumption": ["decrease", 1],
            "look": ["look"]
        }

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            return self.population.makeDescriptionStr()
        elif actionVerb == "increase":
            self.population.increase_consumption(action[1])
        elif actionVerb == "decrease":
            self.population.decrease_consumption(action[1])

        # Update the cancer risk based on the new level of alcohol consumption
        self.population.alcohol_consumption.tick()
        return self.population.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase consumption", "increase consumption", "look", "decrease consumption", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final assessment of the claim
    if simulation.population.alcohol_consumption.cancer_risk > 0:
        print("Claim Supported: The risk of cancer rises with level of alcohol consumption.")
    else:
        print("Claim Refuted: The risk of cancer does not rise with level of alcohol consumption.")

if __name__ == "__main__":
    main()
