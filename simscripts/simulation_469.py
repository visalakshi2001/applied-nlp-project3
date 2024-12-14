
# Claim: Glial calcium waves influence seizures.
# This simulation will test the relationship between astrocyte calcium levels and seizure activity.

from simulation_utils import GameObject, Container

class Astrocyte(GameObject):
    def __init__(self, name, calcium_level=0):
        super().__init__(name)
        self.calcium_level = calcium_level
        self.properties = {
            "calcium_level": calcium_level,
            "is_active": False
        }

    def tick(self):
        # Simulate calcium level changes
        if self.calcium_level > 0:
            self.properties["is_active"] = True
        else:
            self.properties["is_active"] = False

class Neuron(GameObject):
    def __init__(self, name, firing_rate=0):
        super().__init__(name)
        self.firing_rate = firing_rate
        self.properties = {
            "firing_rate": firing_rate,
            "is_firing": False
        }

    def tick(self):
        # Neuron fires if the firing rate is above a threshold
        if self.firing_rate > 0:
            self.properties["is_firing"] = True
        else:
            self.properties["is_firing"] = False

class Seizure(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_occuring": False
        }

    def tick(self, astrocytes):
        # A seizure occurs if at least one astrocyte is active
        self.properties["is_occuring"] = any(astrocyte.properties["is_active"] for astrocyte in astrocytes)

class World(Container):
    def __init__(self):
        super().__init__("brain environment")

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
        astrocyte1 = Astrocyte("astrocyte_1", calcium_level=5)  # Elevated calcium level
        astrocyte2 = Astrocyte("astrocyte_2", calcium_level=0)  # Normal calcium level
        neuron1 = Neuron("neuron_1", firing_rate=1)  # Firing
        seizure = Seizure("seizure_event")

        world.addObject(astrocyte1)
        world.addObject(astrocyte2)
        world.addObject(neuron1)
        world.addObject(seizure)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

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

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Do one tick of the environment
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        astrocytes = [obj for obj in allObjects if isinstance(obj, Astrocyte)]
        seizure = next(obj for obj in allObjects if isinstance(obj, Seizure))

        for obj in allObjects:
            obj.tick()

        seizure.tick(astrocytes)

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check if the seizure is occurring based on astrocyte activity
    seizure_status = "supported" if simulation.rootObject.contains[-1].properties["is_occuring"] else "refuted"
    print(f"The claim that glial calcium waves influence seizures is {seizure_status}.")

if __name__ == "__main__":
    main()
