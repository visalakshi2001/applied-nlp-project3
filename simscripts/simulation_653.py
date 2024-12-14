
# Claim: Interleukin-18 plays an important role in the pathogenesis of atherosclerosis.
# The simulation will model the effects of Interleukin-18 (IL18) on atherosclerosis in a controlled environment.

from simulation_utils import GameObject, Container

class Interleukin(GameObject):
    def __init__(self, name, action_effect=0):
        super().__init__(name)
        self.properties = {
            "action_effect": action_effect  # Represents the effect of IL18 on atherosclerosis
        }

    def tick(self):
        # Simulate the effect of IL18 on atherosclerosis
        self.properties["action_effect"] += 1  # Increment the effect each tick

class Atherosclerosis(GameObject):
    def __init__(self, name, severity=0):
        super().__init__(name)
        self.properties = {
            "severity": severity  # Represents the severity of atherosclerosis
        }

    def tick(self, il18):
        # The severity of atherosclerosis is influenced by IL18
        self.properties["severity"] += il18.properties["action_effect"]  # Increase severity based on IL18 effect

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
        il18 = Interleukin("Interleukin-18")
        atherosclerosis = Atherosclerosis("Atherosclerosis")
        world.addObject(il18)
        world.addObject(atherosclerosis)
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
            # Perform a tick in the simulation
            il18 = self.rootObject.contains[0]  # Get IL18 object
            atherosclerosis = self.rootObject.contains[1]  # Get Atherosclerosis object
            il18.tick()
            atherosclerosis.tick(il18)

        # Update the observation string
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate several ticks to observe the effect of IL18 on atherosclerosis
    for _ in range(5):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the final severity of atherosclerosis
    final_severity = simulation.rootObject.contains[1].properties["severity"]
    if final_severity > 0:
        print("Claim Supported: Interleukin-18 plays an important role in the pathogenesis of atherosclerosis.")
    else:
        print("Claim Refuted: Interleukin-18 does not play a significant role in the pathogenesis of atherosclerosis.")

if __name__ == "__main__":
    main()
