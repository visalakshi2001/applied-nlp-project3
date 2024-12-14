
# Claim: Propriospinal interneurons that play a role in the plastic reorganization of spinal circuits are integral for recovery from spinal cord injury.
# The simulation will model the relationship between propriospinal interneurons and recovery from spinal cord injury.

from simulation_utils import GameObject, Container

class PropriospinalInterneuron(GameObject):
    def __init__(self, name, functional_recovery=0):
        super().__init__(name)
        self.properties = {
            "functional_recovery": functional_recovery
        }

    def tick(self):
        # Simulate the role of propriospinal interneurons in recovery
        self.properties["functional_recovery"] += 1  # Increment recovery over time

    def makeDescriptionStr(self):
        return f"A {self.name} with current functional recovery level: {self.properties['functional_recovery']}."

class SpinalCordInjury(GameObject):
    def __init__(self, name, severity):
        super().__init__(name)
        self.properties = {
            "severity": severity,
            "recovery": 0
        }

    def tick(self):
        # Recovery is influenced by propriospinal interneurons
        if self.contains:
            for interneuron in self.contains:
                self.properties["recovery"] += interneuron.properties["functional_recovery"]

    def makeDescriptionStr(self):
        return f"A {self.name} with severity {self.properties['severity']} and recovery level: {self.properties['recovery']}."

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
        injury = SpinalCordInjury("spinal_cord_injury", severity=10)
        interneuron1 = PropriospinalInterneuron("propriospinal_interneuron_1")
        interneuron2 = PropriospinalInterneuron("propriospinal_interneuron_2")
        
        injury.addObject(interneuron1)
        injury.addObject(interneuron2)
        world.addObject(injury)
        
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
            # Perform a tick to simulate time passing
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate several ticks to observe recovery
    for _ in range(5):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check if recovery level indicates support for the claim
    recovery_level = simulation.rootObject.contains[0].properties["recovery"]
    if recovery_level > 0:
        print("Claim Supported: Propriospinal interneurons are integral for recovery from spinal cord injury.")
    else:
        print("Claim Refuted: Propriospinal interneurons do not contribute to recovery from spinal cord injury.")

if __name__ == "__main__":
    main()
