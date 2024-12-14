
# Claim: Energy balance requires hypothalamic glutamate neurotransmission.
# The simulation will model the relationship between metabolic status, leptin, and glutamate transporters in hypothalamic neurons.

from simulation_utils import GameObject, Container

class Neuron(GameObject):
    def __init__(self, name, glutamate_level=0):
        super().__init__(name)
        self.glutamate_level = glutamate_level
        self.properties = {
            "glutamate_level": glutamate_level,
            "activity": 0
        }

    def tick(self):
        # The activity of the neuron is influenced by the glutamate level
        self.properties["activity"] = self.glutamate_level * 2  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"A {self.name} with glutamate level {self.glutamate_level} and activity {self.properties['activity']}."

class GlialCell(GameObject):
    def __init__(self, name, glucose_transporters=0, glutamate_transporters=0):
        super().__init__(name)
        self.glucose_transporters = glucose_transporters
        self.glutamate_transporters = glutamate_transporters
        self.properties = {
            "glucose_transporters": glucose_transporters,
            "glutamate_transporters": glutamate_transporters
        }

    def modify_transporters(self, metabolic_signal):
        # Modify transporters based on metabolic signals
        self.glutamate_transporters += metabolic_signal
        self.glucose_transporters += metabolic_signal // 2  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"A {self.name} with {self.glucose_transporters} glucose transporters and {self.glutamate_transporters} glutamate transporters."

class World(Container):
    def __init__(self):
        Container.__init__(self, "hypothalamus")

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
        neuron = Neuron("POMC Neuron")
        glial_cell = GlialCell("Astrocyte")
        world.addObject(neuron)
        world.addObject(glial_cell)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("increase metabolic signal", ["increase", 1])
        self.addAction("decrease metabolic signal", ["decrease", 1])

    def actionIncrease(self, metabolic_signal):
        glial_cell = self.rootObject.contains[1]  # Assuming the second object is the glial cell
        glial_cell.modify_transporters(metabolic_signal)
        neuron = self.rootObject.contains[0]  # Assuming the first object is the neuron
        neuron.glutamate_level += glial_cell.glutamate_transporters
        return f"Increased metabolic signal. Glial cell modified transporters. Neuron glutamate level is now {neuron.glutamate_level}."

    def actionDecrease(self, metabolic_signal):
        glial_cell = self.rootObject.contains[1]
        glial_cell.modify_transporters(-metabolic_signal)
        neuron = self.rootObject.contains[0]
        neuron.glutamate_level += glial_cell.glutamate_transporters
        return f"Decreased metabolic signal. Glial cell modified transporters. Neuron glutamate level is now {neuron.glutamate_level}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            self.observationStr = self.actionIncrease(action[1])
        elif actionVerb == "decrease":
            self.observationStr = self.actionDecrease(action[1])

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
    actions = ["look", "increase metabolic signal", "look", "decrease metabolic signal", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
