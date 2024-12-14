
# Claim: Sepsis related mortality has risen from 2009 to 2014.
# The simulation will analyze the trends in sepsis incidence and mortality rates from 2009 to 2014 based on clinical data.

from simulation_utils import GameObject, Container

class SepsisCase(GameObject):
    def __init__(self, year, mortality_rate):
        super().__init__(f"Sepsis Case {year}")
        self.year = year
        self.mortality_rate = mortality_rate

    def tick(self):
        # Simulate the change in mortality rate over the years
        if self.year < 2014:
            self.mortality_rate -= 0.033  # Simulating a decline in mortality rate
        else:
            self.mortality_rate += 0.01  # Simulating a slight increase in mortality rate for 2014

    def makeDescriptionStr(self):
        return f"In {self.year}, the mortality rate was {self.mortality_rate:.2f}."

class World(Container):
    def __init__(self):
        super().__init__("Sepsis Mortality Simulation Environment")
        self.sepsis_cases = []

    def addSepsisCase(self, year, mortality_rate):
        case = SepsisCase(year, mortality_rate)
        self.addObject(case)
        self.sepsis_cases.append(case)

    def calculateMortalityTrend(self):
        # Calculate the trend of mortality rates from 2009 to 2014
        mortality_rates = [case.mortality_rate for case in self.sepsis_cases]
        return mortality_rates

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        # Adding sepsis cases with initial mortality rates
        for year in range(2009, 2015):
            initial_mortality_rate = 0.15  # Starting mortality rate
            world.addSepsisCase(year, initial_mortality_rate)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"], "calculate trend": ["calculate trend"]}

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "calculate trend":
            mortality_trend = self.rootObject.calculateMortalityTrend()
            self.observationStr = f"Mortality rates from 2009 to 2014: {mortality_trend}"
        
        # Do one tick of the environment
        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "calculate trend"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
