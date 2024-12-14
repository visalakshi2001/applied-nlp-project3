
# Claim: Antidepressants increase the severity of migraines.
# The simulation will evaluate the effects of tricyclic antidepressants on migraine severity.

from simulation_utils import GameObject, Container

class Antidepressant(GameObject):
    def __init__(self, name, effectiveness=0, adverse_effects=0):
        super().__init__(name)
        self.properties = {
            "effectiveness": effectiveness,  # Effectiveness in reducing migraine severity
            "adverse_effects": adverse_effects  # Number of adverse effects experienced
        }

    def tick(self):
        # Simulate the effect of the antidepressant over time
        self.properties["effectiveness"] += 1  # Increase effectiveness over time
        self.properties["adverse_effects"] += 1  # Increase adverse effects over time

    def makeDescriptionStr(self):
        description = f"{self.name} has an effectiveness of {self.properties['effectiveness']} in reducing migraine severity and has caused {self.properties['adverse_effects']} adverse effects."
        return description

class Migraine(GameObject):
    def __init__(self, name, severity=10):
        super().__init__(name)
        self.properties = {
            "severity": severity  # Initial severity of the migraine
        }

    def tick(self, antidepressant):
        # Simulate the effect of the antidepressant on migraine severity
        if antidepressant.properties["effectiveness"] > 0:
            self.properties["severity"] -= antidepressant.properties["effectiveness"]  # Reduce severity based on effectiveness
        if antidepressant.properties["adverse_effects"] > 0:
            self.properties["severity"] += antidepressant.properties["adverse_effects"]  # Increase severity based on adverse effects

    def makeDescriptionStr(self):
        description = f"{self.name} has a severity level of {self.properties['severity']}."
        return description

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
        antidepressant = Antidepressant("Tricyclic Antidepressant")
        migraine = Migraine("Migraine")
        world.addObject(antidepressant)
        world.addObject(migraine)        
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

        if action[0] == "tick":
            # Perform a tick in the simulation
            migraine = self.rootObject.contains[1]  # Get the migraine object
            antidepressant = self.rootObject.contains[0]  # Get the antidepressant object
            antidepressant.tick()  # Update antidepressant properties
            migraine.tick(antidepressant)  # Update migraine severity based on antidepressant
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    for _ in range(5):  # Simulate for 5 ticks
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Final evaluation of the claim
    migraine = simulation.rootObject.contains[1]
    if migraine.properties["severity"] > 10:
        print("Claim Refuted: Antidepressants increased the severity of migraines.")
    else:
        print("Claim Supported: Antidepressants did not increase the severity of migraines.")

if __name__ == "__main__":
    main()
