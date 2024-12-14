
# Claim: Cognitive behavioral therapy is an ineffective treatment for insomnia
# The simulation will evaluate the effectiveness of Cognitive Behavioral Therapy (CBT) against a placebo and pharmacological treatment for insomnia.

from simulation_utils import GameObject, Container

class Treatment(GameObject):
    def __init__(self, name, effectiveness=0):
        super().__init__(name)
        self.effectiveness = effectiveness

    def tick(self):
        # Simulate the effectiveness of the treatment over time
        if self.name == "CBT":
            self.effectiveness += 0.1  # CBT improves effectiveness
        elif self.name == "Zopiclone":
            self.effectiveness -= 0.05  # Zopiclone effectiveness decreases over time
        elif self.name == "Placebo":
            self.effectiveness += 0.01  # Placebo has minimal effect

    def makeDescriptionStr(self):
        return f"{self.name} treatment effectiveness: {self.effectiveness:.2f}"

class World(Container):
    def __init__(self):
        Container.__init__(self, "treatment environment")

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
        cbt = Treatment("CBT")
        zopiclone = Treatment("Zopiclone")
        placebo = Treatment("Placebo")
        world.addObject(cbt)
        world.addObject(zopiclone)
        world.addObject(placebo)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"tick": ["tick"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "tick":
            # Perform a tick to simulate the passage of time and treatment effectiveness
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate for a number of ticks to observe the effectiveness over time
    for _ in range(10):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Determine if the claim is supported or refuted based on effectiveness
    cbt_effectiveness = simulation.rootObject.contains[0].effectiveness
    zopiclone_effectiveness = simulation.rootObject.contains[1].effectiveness
    placebo_effectiveness = simulation.rootObject.contains[2].effectiveness

    if cbt_effectiveness > zopiclone_effectiveness and cbt_effectiveness > placebo_effectiveness:
        print("Claim is Refuted: CBT is an effective treatment for insomnia.")
    else:
        print("Claim is Supported: CBT is an ineffective treatment for insomnia.")

if __name__ == "__main__":
    main()
